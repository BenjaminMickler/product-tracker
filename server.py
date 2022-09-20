import websockets
import asyncio
import sqlite3

conn = sqlite3.connect("products.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS products (model TEXT, name TEXT, manufacturer TEXT, price TEXT)")

async def handle(websocket):
    async for message in websocket:
        if "GET ALL" in message:
            c.execute("SELECT * FROM products")
            await websocket.send(str(c.fetchall()))
        elif "GET" in message:
            c.execute("SELECT * FROM products WHERE model = ?", (message.split(" ")[1],))
            await websocket.send(str(c.fetchone()))
        elif "ADD" in message:
            model, name, manufacturer, price = message.split(" ")[1:]
            c.execute("INSERT INTO products VALUES (?, ?, ?, ?)", (model, name, manufacturer, price))
            conn.commit()
            await websocket.send("OK")
        elif "DELETE" in message:
            c.execute("DELETE FROM products WHERE model = ?", (message.split(" ")[1],))
            conn.commit()
            await websocket.send("OK")
        elif "UPDATE" in message:
            model, name, manufacturer, price = message.split(" ")[1:]
            c.execute("UPDATE products SET name = ?, manufacturer = ?, price = ? WHERE model = ?", (name, manufacturer, price, model))
            conn.commit()
            await websocket.send("OK")

async def main():
    async with websockets.serve(handle, "0.0.0.0", 8765):
        await asyncio.Future()

asyncio.run(main())