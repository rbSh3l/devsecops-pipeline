
from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# This fake key matches the exact AWS pattern but bypasses the "EXAMPLE" ignore list!
DATABASE_PASSWORD = "super_secret_password_123"
API_KEY = "AKIA1234567890ABCDEF" 

def get_db():
    conn = sqlite3.connect("app.db")
    return conn

@app.route("/")
def home():
    return "Welcome to the DevSecOps Demo App"

@app.route("/user")
def get_user():
    # Vulnerable SQL Injection
    username = request.args.get("name")
    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return str(result)

@app.route("/debug")
def debug_info():
    return {
        "database_password": DATABASE_PASSWORD,
        "environment": dict(os.environ),
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
