-- "content".permissions definition

-- Drop table

-- DROP TABLE "content".permissions;

CREATE TABLE "content".permissions (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" varchar(150) NOT NULL,
	CONSTRAINT permissions_id_pk PRIMARY KEY (id)
);


-- "content".roles definition

-- Drop table

-- DROP TABLE "content".roles;

CREATE TABLE "content".roles (
	"name" varchar(150) NULL,
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	CONSTRAINT roles_id_pk PRIMARY KEY (id)
);


-- "content".users definition

-- Drop table

-- DROP TABLE "content".users;

CREATE TABLE "content".users (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	first_name varchar(150) NOT NULL,
	last_name varchar(150) NOT NULL,
	email varchar(254) NOT NULL,
	"password" varchar(128) NOT NULL,
	last_login timestamptz NULL,
	is_superuser bool NOT NULL,
	CONSTRAINT users_id_pk PRIMARY KEY (id)
);
CREATE UNIQUE INDEX users_email_idx ON content.users USING btree (email);


-- "content".roles_permissions definition

-- Drop table

-- DROP TABLE "content".roles_permissions;

CREATE TABLE "content".roles_permissions (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	role_id int4 NOT NULL,
	permission_id int4 NOT NULL,
	CONSTRAINT roles_permissions_perm_id_fk FOREIGN KEY (permission_id) REFERENCES "content".permissions(id) ON DELETE CASCADE,
	CONSTRAINT roles_permissions_role_id_fk FOREIGN KEY (role_id) REFERENCES "content".roles(id) ON DELETE CASCADE
);


-- "content".user_roles definition

-- Drop table

-- DROP TABLE "content".user_roles;

CREATE TABLE "content".user_roles (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	role_id int4 NOT NULL,
	user_id int4 NOT NULL,
	CONSTRAINT user_roles_roles_id_fk FOREIGN KEY (role_id) REFERENCES "content".roles(id) ON DELETE CASCADE,
	CONSTRAINT user_roles_user_id_fk FOREIGN KEY (id) REFERENCES "content".users(id) ON DELETE CASCADE
);


-- "content".user_sessions definition

-- Drop table

-- DROP TABLE "content".user_sessions;

CREATE TABLE "content".user_sessions (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	user_id int4 NOT NULL,
	CONSTRAINT user_sessions_fk FOREIGN KEY (user_id) REFERENCES "content".users(id) ON DELETE CASCADE
);
