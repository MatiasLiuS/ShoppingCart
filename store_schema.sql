-- To reset the database, run this command in the Shell: 
--   sqlite3 myDatabase.db ".read store_schema.sql"

PRAGMA foreign_keys=off;

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
  c_name        varchar(50) not null PRIMARY KEY,
  c_image       varchar(50) not null
);

DROP TABLE IF EXISTS product;
CREATE TABLE product (
  p_id          varchar(32) not null PRIMARY KEY,
  p_name        varchar(50) not null,
  p_price       decimal(24,2) not null,
  p_desc        varchar(200) not null,
  p_inventory   int(50) not null,
  category      varchar(50) not null, 
  p_image       varchar(100) not null,
  FOREIGN KEY(category) references categories (name)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  username        varchar(50) not null PRIMARY KEY,
  password        varchar(50) not null,
  name            varchar(50) not null
);

DROP TABLE IF EXISTS order_history;
CREATE TABLE order_history(
  o_id       varchar(50) not null primary key,
  uname    varchar(50) not null,
  o_date      TEXT NOT NULL,
   total_cost    DECIMAL(10, 2) NOT NULL,
  foreign key(uname) references users(username)

);

DROP TABLE IF EXISTS orderItem;
CREATE TABLE orderItem(
  ord_id       varchar(50) not null,
  usr_name    varchar(50) not null,
  ord_date      varchar(50) not null,
  prod_id      varchar(50) not null, 
  quantity   int not null,
  PRIMARY KEY(ord_id,prod_id),
  foreign key(usr_name) references users(username),
  foreign key(prod_id) references product(id)
  foreign key(ord_id) references orderObj(id)
);


----------------------------Start User Values----------------------------

INSERT INTO users VALUES ("testuser", "testpass", "Matias Liu Schmid");
INSERT INTO users VALUES ("Leah", "LeahBonita", "Leah Liu Schmid");

----------------------------End User Values----------------------------

----------------------------Start Category Values----------------------------

INSERT INTO categories VALUES ('Rings', 'images/catimg/category_rings.jpg');
INSERT INTO categories VALUES ('Necklaces', 'images/catimg/category_necklaces.jpg');
INSERT INTO categories VALUES ('Earrings', 'images/catimg/category_earrings.jpg');

----------------------------End Category Values----------------------------


--Rings--
INSERT INTO product VALUES ('000001', 'Ring_1', 25.00,'This is a cool ring 1', 10, 'Rings','images/pimg/rimg/ring_1.jpg');
INSERT INTO product VALUES ('000002', 'Ring_2', 30.00,'This is a cool ring 2', 10, 'Rings','images/pimg/rimg/ring_2.jpg');
INSERT INTO product VALUES ('000003', 'Ring_3', 35.00, 'This is a cool ring 3',10, 'Rings','images/pimg/rimg/ring_3.jpg');
INSERT INTO product VALUES ('000004', 'Ring_4', 40.00, 'This is a cool ring 4', 10, 'Rings','images/pimg/rimg/ring_4.jpg');

--Necklaces--
INSERT INTO product VALUES ('000010', 'Necklace_1', 25.00,'This is a cool Necklace 1', 10, 'Necklaces','images/pimg/nimg/necklace_1.jpg');
INSERT INTO product VALUES ('000020', 'Necklace_2', 30.00,'This is a cool Necklace 2', 10, 'Necklaces','images/pimg/nimg/necklace_2.jpg');
INSERT INTO product VALUES ('000030', 'Necklace_3', 35.00,'This is a cool Necklace 3', 10, 'Necklaces','images/pimg/nimg/necklace_3.jpg');
INSERT INTO product VALUES ('000040', 'Necklace_4', 40.00,'This is a cool Necklace 4', 10, 'Necklaces','images/pimg/nimg/necklace_4.jpg');

--Product--
INSERT INTO product VALUES ('000100', 'Earring_1', 25.00, 'This is a cool Earring 1', 10, 'Earrings','images/pimg/eimg/earring_1.jpg');
INSERT INTO product VALUES ('000200', 'Earring_2', 30.00, 'This is a cool Earring 2', 10, 'Earrings','images/pimg/eimg/earring_2.jpg');
INSERT INTO product VALUES ('000300', 'Earring_3', 35.00, 'This is a cool Earring 3', 10, 'Earrings','images/pimg/eimg/earring_3.jpg');
INSERT INTO product VALUES ('000400', 'Earring_4', 40.00, 'This is a cool Earring 4', 10, 'Earrings','images/pimg/eimg/earring_4.jpg');

----------------------------End Product Values----------------------------

