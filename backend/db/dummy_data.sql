/*make dummy users*/
insert into users (username, password) values ("user1", "password123");
insert into users (username, password) values ("user2", "password123");
insert into users (username, password) values ("user3", "password123");

/*get user ids of users just created*/
select user_id into @user1 from users where username="user1";
select user_id into @user2 from users where username="user2";
select user_id into @user3 from users where username="user3";

/*create initial list items*/
insert into grocery_list (item_name, created_by) values ("Cake", @user1);
insert into grocery_list (item_name, created_by) values ("Coffee", @user1);
insert into grocery_list (item_name, created_by) values ("Bleach", @user1);

insert into grocery_list (item_name, created_by) values ("Sugar", @user2);
insert into grocery_list (item_name, created_by) values ("Milk", @user2);
insert into grocery_list (item_name, created_by) values ("Orange Juice", @user2);

insert into grocery_list (item_name, created_by) values ("Eggs", @user3);
insert into grocery_list (item_name, created_by) values ("Flour", @user3);
insert into grocery_list (item_name, created_by) values ("Chocolate Chips", @user3);