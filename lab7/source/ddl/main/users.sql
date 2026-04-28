create table users
(
  id       integer not null
    constraint users_pk
      primary key autoincrement,
  name     text,
  username text    not null
    constraint users_unique_username
      unique,
  password text    not null,
  role_id  integer not null
    constraint users_roles_id_fk
      references roles
);

INSERT INTO users (id, name, username, password, role_id)
VALUES (1, 'admin', 'admin', '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', 1);
