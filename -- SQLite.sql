DROP TABLE IF EXISTS `settings`;
CREATE TABLE IF NOT EXISTS `settings` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `daily_limit` VARCHAR(45) NOT NULL,
  `monthly_limit` VARCHAR(45) NOT NULL);

INSERT INTO settings (daily_limit, monthly_limit) VALUES (15, 1200);
SELECT * FROM settings;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `settings_id` INTEGER NOT NULL,
  CONSTRAINT `fk_user_settings`
    FOREIGN KEY (`settings_id`)
    REFERENCES `settings` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

INSERT INTO user (name, surname, username, password, settings_id) VALUES ('Ivan', 'Sergeyev', 'ivan2002', 'password123', 1);
SELECT * FROM user;

DROP TABLE IF EXISTS `item`;
CREATE TABLE IF NOT EXISTS `item` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `item` VARCHAR(45) NOT NULL,
  `price` DECIMAL NOT NULL,
  `description` TEXT NULL
  );

INSERT INTO item (item, price, description) VALUES ('Leap card', 60, 'Card for leap');
INSERT INTO item (item, price, description) VALUES ('Guinness', 2.5, 'An excellent beer');
INSERT INTO item (item, price, description) VALUES ('Beamish', 2.5, 'An even better beer');
INSERT INTO item (item, price, description) VALUES ('Joks', 10, 'Do not put them with socks!');
INSERT INTO item (item, price, description) VALUES ('Wombat', 100, 'Derek doesn t like those');
INSERT INTO item (item, price, description) VALUES ('Iron maiden album(Number of the Beast)', 666, 'I walked alone, my mind was blank. I needed time to think to get the memories from my mind...');

SELECT * FROM item;

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `category` VARCHAR(45) NOT NULL,
  `user_id` INTEGER NOT NULL,
   CONSTRAINT `fk_category_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
  );

INSERT INTO category (category, user_id) VALUES ('Travel', 1);
INSERT INTO category (category, user_id) VALUES ('Fun', 1);
INSERT INTO category (category, user_id) VALUES ('Medication', 1);
INSERT INTO category (category, user_id) VALUES ('Music', 1);

SELECT * FROM category;

DROP TABLE IF EXISTS `summary`;
CREATE TABLE IF NOT EXISTS `summary` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user_id` INT NOT NULL,
  `item_id` INT,
  `category_id` INT NOT NULL,
  `date` VARCHAR(20) NOT NULL,
  CONSTRAINT `fk_summary_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_summary_item1`
    FOREIGN KEY (`item_id`)
    REFERENCES `item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_summary_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `category` (`id`)
    ON DELETE CASCADE 
    ON UPDATE NO ACTION);

INSERT INTO summary (user_id, item_id, category_id, date) VALUES (1, 1, 1, '24.2.2023');
INSERT INTO summary (user_id, item_id, category_id, date) VALUES (1, 2, 3, '24.2.2023');
INSERT INTO summary (user_id, item_id, category_id, date) VALUES (1, 3, 3, '24.2.2023');
INSERT INTO summary (user_id, item_id, category_id, date) VALUES (1, 4, 2, '24.2.2023');
INSERT INTO summary (user_id, item_id, category_id, date) VALUES (1, 5, 3, '24.2.2023');
INSERT INTO summary (user_id, item_id, category_id, date) VALUES (1, 6, 4, '24.2.2023');
INSERT INTO summary (user_id, item_id, category_id, date) VALUES (1, 6, 4, '25.2.2023');
INSERT INTO summary (user_id, item_id, category_id, date) VALUES (1, 6, 4, '25.2.2023');
INSERT INTO summary (user_id, item_id, category_id, date) VALUES (1, 4, 2, '27.2.2023');

SELECT * FROM summary;

CREATE TRIGGER IF NOT EXISTS trg_delete_summary
AFTER DELETE ON category
BEGIN
  DELETE FROM summary WHERE category_id = OLD.id;
END;


