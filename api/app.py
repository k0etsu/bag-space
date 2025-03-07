from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
import psycopg2

import db_func


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

load_dotenv()

dbconn = {
    "database": "flask_db",
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "port": 5432
}

db_conn = psycopg2.connect(**dbconn)


@app.get("/get_items")
def get_items():
    items = db_func.get_items(db_conn)
    rows = []
    for item in items:
        rows.append(
            {
                "id": item[0],
                "name": item[1],
                "category": item[2],
                "stock": item[3],
                "notes": item[4]
            }
        )
    return jsonify(rows)


@app.post("/add_item")
def add_item():
    if request.mimetype != "application/json":
        return "Bad Request", 400
    try:
        params = request.get_json()
        assert "name" in params
        assert "category" in params
        assert "stock" in params
        assert "notes" in params

        db_func.add_item(db_conn, params)

        return "Inserted row into DB", 200
    except AssertionError as e:
        return "Incorrect json", 400
    except:
        return "Bad Request", 400


@app.post("/update_item")
def update_item():
    if request.mimetype != "application/json":
        return "Bad Request", 400
    try:
        params = request.get_json()
        assert "id" in params
        assert "type" in params
        if params["type"] == "inc":
            db_func.inc_stock(db_conn, params)
        elif params["type"] == "dec":
            db_func.dec_stock(db_conn, params)
        elif params["type"] == "update":
            try:
                assert "name" in params
                assert "category" in params
                assert "stock" in params
                assert "notes" in params
                db_func.update_item(db_conn, params)
            except AssertionError:
                return "Incorrect json", 400
        return "Updated item", 200
    except AssertionError:
        return "Missing ID", 400


@app.delete("/delete_item")
def delete_item():
    if request.mimetype != "application/json":
        return "Bad Request", 400
    try:
        params = request.get_json()
        assert "id" in params

        db_func.delete_item(db_conn, params)

        return "Deleted row from DB", 200
    except AssertionError as e:
        return "Incorrect json", 400
    except Exception as e:
        print(e)
        return "Bad Request", 400


if __name__ == "__main__":
    app.run(host=os.getenv("localhost"), port="5000")
