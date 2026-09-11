# Stack detection and extraction recipes

Load ONLY the playbook that matches the detected stack. Always also load `raw-sql.md`.

## 0. Detect stack

Scan the project root (do not recurse into node_modules, venv, target, dist, .git).

| Signal | lang | framework | orm |
|---|---|---|---|
| `pom.xml` / `build.gradle` + `spring-boot` | java | spring | jpa if `spring-data-jpa`, mybatis if `mybatis` / `mybatis-plus` |
| `requirements.txt` / `pyproject.toml` + `fastapi` | py | fastapi | sqlalchemy / sqlmodel / prisma / tortoise |
| `manage.py` + `DJANGO_SETTINGS_MODULE` / `django` | py | django | django-orm |
| `package.json` + `@nestjs/core` | ts | nest | prisma / typeorm / drizzle / sequelize |
| `package.json` + `express` / `fastify` / `koa` | ts/js | express-like | same |
| `schema.prisma` / `@prisma/client` | * | * | prisma |
| `go.mod` + `gin-gonic/gin` | go | gin | gorm if `gorm.io/gorm` |
| `*.xml` mapper under `resources` + `Mapper.java` | java | spring | mybatis |

Write `meta.stack` before extracting anything.

## 1. Schema ground truth (all stacks)

Priority, stop at the first complete source:

1. Live DB `information_schema` / `pg_catalog` (SELECT only). Tier = T1. `information_schema.columns.column_comment` (MySQL) or the Postgres column description gives `desc` for free.
2. Migrations / DDL. Don't rely on filename conventions alone — grep the whole repo (excluding `node_modules`/`.venv`/`vendor`/`target`/`dist`/`build`/`.git`) for `CREATE TABLE` case-insensitively and treat every hit as a DDL source, regardless of what the file is called. Known locations to check first: `**/db/migration/*.sql`, `**/alembic/versions/*.py`, `**/prisma/migrations/**`, `**/flyway/**`, `**/*schema*.sql`, any `sql/`, `db/`, `scripts/sql/`, or repo-root `*.sql` dump. Tier = T2. Each column's trailing `COMMENT '...'` (MySQL) or a separate `COMMENT ON COLUMN t.c IS '...'` (Postgres) is the `desc` — read it straight off the same `CREATE TABLE` you're already parsing for columns/types. If no `CREATE TABLE` exists anywhere in the repo, there is no DDL source — move on to ORM models and leave `desc` unset rather than searching harder for a filename that doesn't exist.
3. ORM models. Tier = T3.
4. SQL strings harvested from code. Tier = T4.

For every table capture: name, schema, fields (name, type, pk, uk, nullable, fk, desc — see `Desc:` line in each recipe below and "Field descriptions" in `references/ir-schema.md`).

## 2. API inventory (all stacks)

Prefer OpenAPI / Swagger / SpringDoc if present (`openapi.yaml`, `/v3/api-docs`, `@Operation`).
Otherwise scan routers / controllers (see per-stack playbooks).

Endpoint `id` format: `"{METHOD} {path}"`, path params kept as `{id}` / `:id`.

## 3. Handler → DB walk

From each handler, follow callees 2–4 levels: controller → service → repository / mapper.

Stop at: JDK / CPython / Node stdlib, Spring / Django / FastAPI / Express framework code, generated Prisma client internals.

For each DB touch emit an `EndpointTable` with `evidence` = `file:line`.

## 4. Per-stack recipes

### Java / Spring / JPA
- Routes: `@RequestMapping` `@GetMapping` `@PostMapping` `@PutMapping` `@PatchMapping` `@DeleteMapping`
- Tables: `@Entity` `@Table(name=)` default = class name
- Access: `JpaRepository` / `CrudRepository` method names, `save`/`delete`/`find*`, `@Query` JPQL/native
- Fields: entity fields + `@Column(name=)`; JPQL SELECT list; derived query tokens (`findByUserId` → `user_id`)
- Desc: DDL `COMMENT`, Hibernate `@Comment`, Swagger `@ApiModelProperty(value=)` / `@Schema(description=)`, or the Javadoc/line comment directly above the field (common in RuoYi-style entities, e.g. `/** 用户昵称 */`)

### Java / Spring / MyBatis / Plus
- Routes: same as Spring MVC
- Access: mapper Java interface method → XML `<select|insert|update|delete id>` or `@Select/@Insert/...`
- Table names: FROM / INTO / UPDATE / DELETE FROM in XML, plus `@TableName` on entity
- Includes: expand `<include refid>` before parsing
- Plus: `BaseMapper<T>` / `ServiceImpl<M,T>` → resolve T; `QueryWrapper` / `LambdaQueryWrapper.eq(Entity::getX)`
- Dynamic: `${tableName}` or `${ew.customSqlSegment}` → confidence=uncertain
- Desc: same as JPA above — DDL `COMMENT`, `@ApiModelProperty(value=)`, or the doc-comment above the entity field

### Python / FastAPI / SQLAlchemy / SQLModel
- Routes: `@app.get/post/put/patch/delete`, `APIRouter`
- Access: `session.query(Model)`, `select(Model)`, `session.add`, `session.delete`, `session.execute(text(...))`
- Table: `Model.__tablename__` or SQLModel `table=True`
- Fields: `Model.columns`, `with_entities`, insert dict keys
- Desc: `Column(..., comment=)` (SQLAlchemy), `Field(description=)` (Pydantic/SQLModel), or DB column comment

### Python / Django
- Routes: `urls.py` `path()` / `router.register` ViewSet actions
- Access: `Model.objects.filter/get/create/update/delete`, `QuerySet.raw()`, `connection.cursor()`
- Fields: `Meta.fields`, `only()` / `values()`, serializer fields, model `_meta.get_fields()`
- Desc: field `verbose_name` (Django's own human-readable label) or `help_text`

### Node / Prisma
- Routes: Nest `@Controller` + method verbs; Express `router.get/post`
- Access: `prisma.user.findMany/create/update/deleteMany/upsert`
- Table: `model User { @@map("users") }` else model name
- Fields: `select` / `include` / `data` keys
- Desc: `///` triple-slash doc-comment directly above the field in `schema.prisma`

### Node / TypeORM / Drizzle / Sequelize
- TypeORM: `@Entity` `@Column` `repo.find/save` `createQueryBuilder().from().select().where()`
- Drizzle: `pgTable(...)` `db.select().from(table)` `db.insert(table)` `db.update(table)`
- Sequelize: `Model.findAll/create/update/destroy` `attributes:[]`
- Desc: TypeORM `@Column({ comment: })`; Drizzle/Sequelize usually have none — fall back to DB column comment if a live DB or DDL is available

### Go / Gin / GORM
- Routes: `r.GET/POST/PUT/PATCH/DELETE`
- Access: `db.Find/First/Create/Updates/Delete/Save(&Model)`
- Table: `TableName()` or snake plural of struct
- Fields: struct fields + `gorm:"column:x"` tags
- Desc: `gorm:"comment:..."` tag, or the line comment after the struct field (Go convention)

## 5. Field-level relations

1. Schema FK columns (source=`fk`, highest trust)
2. JOIN ... ON a.x = b.y in traced SQL (source=`join`)
3. Shared where-key used across two models in one handler (source=`inferred`, confidence ≤ med)
4. DTO / serializer field maps (`@Column`, `source=`, `column=`) only attach fields to an already-known table

Cardinality default: FK child→parent = N:1. Unique FK = 1:1. Join table with two FKs = N:M.

## 6. What not to do

- Do not execute INSERT/UPDATE/DELETE against a live DB
- Do not guess a table name from a variable
- Do not treat log tables / audit interceptors as the primary write unless the handler calls them
- Do not traverse `node_modules`, `.venv`, `venv`, `target`, `dist`, `build`, `__pycache__`, `.git`, `vendor`
