-- create transactional db
CREATE DATABASE oltp;

-- connect to db
\c oltp

-- create tables
CREATE TABLE IF NOT EXISTS customers (
       customer_id serial primary key,
       first_name varchar(70),
       last_name varchar(70),
       phone_number varchar(15),
       curp varchar(18),
       rfc varchar(13),
       address varchar(255)
       );

CREATE TABLE IF NOT EXISTS items (
       item_id serial primary key,
       item_name varchar(255),
       item_price real
       );

CREATE TABLE IF NOT EXISTS orders (
       order_id serial,
       date timestamp,
       price real,
       comments varchar(255),
       customer_id int not null,
       item_id int not null,
       FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
       FOREIGN KEY (item_id) REFERENCES items (item_id)
       );

-- insert values into tables
INSERT INTO
       customers (first_name, last_name, phone_number, curp, rfc, address)
VALUES
  ('Jerry', 'Seinfeld', '555-8383', 'SEIJ540429HNYDLS04', 'SEIJ540529BB8', '129 W 81st St, New York, NY 10024'),
  ('George', 'Costanza', '555-8383', 'COSG580420HNYDLS03', 'COSG580420KU9', '22-37 37th St, Astoria, NY 11103'),
  ('Cosmo', 'Kramer', '555-3455', 'KRAC490724HNYDLS01', 'KRAC490724788', '129 W 81st St, New York, NY 10024');

INSERT INTO
       items (item_name, item_price)
VALUES
  ('The Coffee Table Book About Coffee Tables', 12.99),
  ('Oil Tanker Bladder', 4999.99),
  ('Ketchup & Mustard in the Same Bottle', 10.99),
  ('The Bro', 129453.00);

INSERT INTO
       orders (date, price, comments, customer_id, item_id)
VALUES
  ('1994-05-19 21:00:00-5', 12.99, 'The Opposite, Kramerica Industries', 1, 1),
  ('1997-10-02 21:00:00-5', 10.99, 'The Voice, Kramerica Industries', 1, 3),
  ('1997-10-02 21:15:00-5', 4999.99, 'The Voice, Kramerica Industries', 3, 2);

ALTER ROLE postgres WITH PASSWORD 'P4ssw0rd!';
