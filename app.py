from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# INTENTIONAL VULNERABILITY: Hardcoded secret (Gitleaks will catch this)
DATABASE_PASSWORD = "super_secret_password_123"
API_KEY = os.environ.get("API_KEY", "not-set")
    

def get_db():
    conn = sqlite3.connect("app.db")
    return conn

@app.route("/")
def home():
    return "Welcome to the DevSecOps Demo App"

@app.route("/user")
def get_user():
    # INTENTIONAL VULNERABILITY: SQL Injection (Semgrep will catch this)
    username = request.args.get("name")
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    
    result = cursor.fetchone()
    conn.close()
    return str(result)

@app.route("/debug")
def debug_info():
    # INTENTIONAL VULNERABILITY: Information disclosure
    return {
        "database_password": DATABASE_PASSWORD,
        "environment": dict(os.environ),
    }

if __name__ == "__main__":
    # INTENTIONAL VULNERABILITY: Debug mode enabled in production
    app.run(host="0.0.0.0", port=5000, debug=True)