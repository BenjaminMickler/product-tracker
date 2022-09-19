import sqlite3
import datetime
import sys
import re

serial = repr(input('Model: '))

conn = sqlite3.connect('devices.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS devices (serial TEXT, date TEXT, product_name TEXT, manufacturer TEXT, manufacturer_price TEXT)")

def input_details():
    price = input("Price: ")
    date = datetime.datetime.now()
    store = input("Store: ")
    c.execute("SELECT store FROM {} WHERE store = ?".format(serial), (store,))
    if not c.fetchone():
        c.execute("INSERT INTO {} VALUES (?, ?, ?)".format(serial), (price, date, store))
    else:
        c.execute("UPDATE {} SET price = ?, date = ? WHERE store = ?".format(serial), (price, date, store))
    c.execute("SELECT serial FROM devices WHERE serial = ?", (serial,))
    if not c.fetchone():
        product_name = input("Product name: ")
        manufacturer = input("Manufacturer: ")
    c.execute("INSERT INTO devices VALUES (?, ?, ?, ?)", (serial, date, product_name, manufacturer))
    conn.commit()

while True:
    c.execute("SELECT * FROM devices WHERE serial = ?", (serial,))
    data = c.fetchone()
    c.execute("CREATE TABLE IF NOT EXISTS {} (price TEXT, date TEXT, store TEXT)".format(serial))
    c.execute("SELECT * FROM {}".format(serial))
    data2 = c.fetchall()
    if data:
        print("-------------------")
        print(f"Model: {data[0]}")
        print(f"Product name: {data[2]}")
        print(f"Manufacturer: {data[3]}")
        print("----------\n| Stores |\n----------")
        data2.sort(key=lambda x: x[0])
        for row in data2:
            print(f"Store: {row[2]}")
            print(f"Price: A${row[0]}")
            print(f"Date: {datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')}")
            print("----------")
            options = input("Options: \n1. Add new store\n2. Delete store\n3. Exit\n4. Delete database\n5. Set manufacturer price\n> ")
            match options:
                case "1":
                    input_details()
                case "2":
                    store = input("Store: ")
                    c.execute("DELETE FROM {} WHERE store = ?".format(serial), (store,))
                    conn.commit()
                case "3":
                    sys.exit(0)
                case "4":
                    # delete database
                    c.execute("DROP TABLE IF EXISTS devices")
                    c.execute("DROP TABLE IF EXISTS {}".format(serial))
                    conn.commit()
                    sys.exit(0)
                case "5":
                    man_price = input("Manufacturer price: ")
                case _:
                    print("Invalid option")
    else:
        input_details()