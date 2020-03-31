create database if not exists LinkedinJobAlerts;

use LinkedinJobAlerts;

create table jobs (
  id int primary key auto_increment,
  link varchar(500),
  company varchar(100),
  title varchar(250),
  post_time int(11),
  type int -- 1 - intern, 2 - new grad, 3 - other
);
