create table users
(
  id            integer                       not null
    constraint users_pk
      primary key autoincrement,
  name          text,
  username      text                          not null
    constraint users_unique_username
      unique,
  password      text                          not null,
  last_modified INTEGER default (unixepoch()) not null,
  role_id       integer                       not null
    constraint users_roles_id_fk
      references roles
);
