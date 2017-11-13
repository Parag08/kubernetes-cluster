drop table if exists machine_table;
drop table if exists user_table;
drop table if exists cluster_table;

create table user_table (
  id integer primary key autoincrement,
  name text not null,
  userName text not null,
  userEmail text not null,
  timeStamp text not null
);

create table machine_table (
  id integer primary key autoincrement,
  name text not null,
  hostType text,
  authType text not null,
  userName text not  null,
  password text,
  publicIP text not null,
  privateIP text not null,
  network text,
  keys text,
  rack text,
  geograph text,
  CPU text,
  RAM text,
  Disk text
);


create table cluster (
  id integer primary key autoincrement,
  name text not null,
  description text,
  organisation text,
  master_id integer,
  machine_id integer,
  FOREIGN KEY (master_id) REFERENCES user_table
  FOREIGN KEY (machine_id) REFERENCES machine_table
);
