
CREATE TABLE IF NOT EXISTS foods (
	food_id text PRIMARY KEY,
   	food text
);

INSERT INTO foods (food_id, food)
VALUES
	('F01', 'Kubideh'),
	('F02', 'Sultani'),
	('F03', 'Fischteller'),
	('F04', 'Lammhaxe'),
	('F05', 'Tabbouleh');

CREATE TABLE IF NOT EXISTS drinks (
	drink_id text PRIMARY KEY,
   	drink text
);

INSERT INTO drinks (drink_id, drink)
VALUES
	('D01', 'Ayran'),
	('D02', 'Boza'),
	('D03', 'Turkish_Coffee'),
	('D04', 'Turkish_Tea'),
	('D05', 'Turkish_Raki');

CREATE TABLE IF NOT EXISTS reports (
	no INTEGER PRIMARY KEY AUTOINCREMENT,
   	food_id text,
    drink_id text,
    food_qty integer,
    drink_qty integer,
    date text,
    FOREIGN KEY(food_id) REFERENCES food(food_id),
    FOREIGN KEY(drink_id) REFERENCES drink(drink_id)
);

-------------------------------------------------------------------------------------------

c.execute("INSERT INTO reports VALUES (:food_id, :drink_id, :food_qty, :drink_qty, :date)",
	{'food_id' : x,
	 'drink_id' : y,
	 'food_qty' : z,
	 'drink_qty' : a,
	 'date' : b
	 }
conn.commit()
conn.close()

------------------------------------------------------------------------------------------

