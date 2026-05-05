create table roles
(
  id   integer not null
    constraint roles_pk
      primary key autoincrement,
  role text    not null
    constraint roles_unique_role
      unique
);

INSERT INTO roles (id, role)
VALUES (1, 'admin');
INSERT INTO roles (id, role)
VALUES (2, 'user');
