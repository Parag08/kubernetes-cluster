drop table if exists Config_meta_table;
drop table if exists user_table;
create table Config_meta_table (
  id integer primary key autoincrement,
  Name text not null,
  UIName text not null,
  Description text not null,
  DefaultValue text not null,
  Required integer not null,
  datatype text not null,
  timestamp text not null,
  editedby integer not null,
  CONSTRAINT FK_user FOREIGN KEY (editedby)
    REFERENCES user_table (id) ON DELETE CASCADE ON UPDATE RESTRICT
);

create table user_table (
  id integer primary key autoincrement,
  Name text not null,
  username text not null,
  useremail text not null,
  timestamp text not null
);
