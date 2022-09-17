create database home_dashboard;

-- create user 'lamp_user'@'localhost' identified by 'password123';
-- grant all privileges on *.* to 'lamp_user'@'localhost';
-- flush privileges;

use home_dashboard;

create table users(
    user_id int not null auto_increment,
    username varchar(80) not null,
    password varchar(255) not null,
    created_at datetime default current_timestamp,
    unique(username),
    primary key(user_id)
);

create table grocery_list(
    item_id int not null auto_increment,
    item_name varchar(80) not null,
    created_at datetime default current_timestamp,
    created_by int not null,
    unique(item_name),
    foreign key(created_by) references users(user_id),
    primary key(item_id)
);