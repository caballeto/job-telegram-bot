create database if not exists LinkedinJobAlerts;

use LinkedinJobAlerts;

  create table jobs (
    id int primary key auto_increment,
    link varchar(500) unique,
    company varchar(100),
    title varchar(250),
    post_time int(11),
    type int -- 1 - intern, 2 - new grad, 3 - other
  );

create table proposals (
  id int primary key auto_increment,
  link text,
  posted_by varchar(200)
);
