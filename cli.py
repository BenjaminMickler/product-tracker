import sqlite3
import datetime
import sys
import re
import signal

print("press \033[1mctrl+c\033[0m at any time to exit\n")

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

while True:
    serial = repr(input('Product Model: ')).replace("'", "")
    conn = sqlite3.connect('devices.db')
    c = conn.cursor()
    if serial == "ALL":
        c.execute("SELECT * FROM devices")
        for row in c.fetchall():
            # print in a table format
            print('{:20} {:35} {:30} {:20}'.format(*row))
        break
    c.execute("CREATE TABLE IF NOT EXISTS devices (serial TEXT, date TEXT, product_name TEXT, manufacturer TEXT)")

    c.execute("SELECT manufacturer FROM devices WHERE serial = ?", (serial,))
    man = c.fetchone()
    if man is None:
        manufacturer = input("Manufacturer: ")
    else:
        manufacturer = man[0]
    c.execute("SELECT product_name FROM devices WHERE serial = ?", (serial,))
    pn = c.fetchone()
    if pn is None:
        product_name = input("Product Name: ")
    else:
        product_name = pn[0]
    c.execute("INSERT INTO devices VALUES (?, ?, ?, ?)", (serial, datetime.datetime.now(), product_name, manufacturer))
    conn.commit()

    def input_details():
        price = input("Price: ")
        date = datetime.datetime.now()
        store = input("Store: ")
        c.execute("SELECT store FROM {} WHERE store = ?".format(serial), (store,))
        if not c.fetchone():
            c.execute("INSERT INTO {} VALUES (?, ?, ?)".format(serial), (price, date, store))
        else:
            c.execute("UPDATE {} SET price = ?, date = ? WHERE store = ?".format(serial), (price, date, store))
        conn.commit()
        c.execute("UPDATE devices SET date = ? WHERE serial = ?", (date, serial))
        conn.commit()

    while True:
        c.execute("SELECT * FROM devices WHERE serial = ?", (serial,))
        data = c.fetchone()
        c.execute("CREATE TABLE IF NOT EXISTS {} (price TEXT, date TEXT, store TEXT)".format(serial))
        c.execute("SELECT * FROM {}".format(serial))
        data2 = c.fetchall()
        if data:
            print("-------------------")
            print(f"Product Model: {data[0]}")
            print(f"Product Name: {data[2]}")
            print(f"Manufacturer: {data[3]}")
            c.execute("SELECT store FROM {} WHERE store = ?".format(serial), (data[3],))
            manprice = c.fetchone()
            if not manprice:
                manprice = "\033[1mnot set\033[0m"
            else:
                c.execute("SELECT price FROM {} WHERE store = ?".format(serial), (data[3],))
                manprice = c.fetchone()[0]
            data2.sort(key=lambda x: x[0])
            if manprice == "\033[1mnot set\033[0m":
                print(f"Manufacturer Price: {manprice}")
            else:
                price_difference = int(manprice)-int(data2[0][0])
                price_difference_percent = round(price_difference/int(manprice)*100, 1)
                print(f"Best Price Deal: A${price_difference}, {price_difference_percent}%")
            print("----------\n| Stores |\n----------")
            for row in data2:
                print(f"Store: {row[2]}")
                print(f"Price: A${row[0]}")
                print(f"Date: {datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')}")
                print("----------")
            options = input("Options: \n1. Add new store\n2. Delete store\n3. Exit\n4. Delete database\n5. Restart\n> ")
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
                    c.execute("DROP TABLE IF EXISTS devices")
                    c.execute("DROP TABLE IF EXISTS {}".format(serial))
                    conn.commit()
                    sys.exit(0)
                case "5":
                    break
                case _:
                    print("Invalid option")
        else:
            input_details()
