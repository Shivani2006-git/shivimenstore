from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# 1. Database connection
# IMPORTANT: Change 'yourpassword' to your real MySQL password!
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root", 
        database="my_test_db"
    )
    print("✅ Connected to MySQL successfully!")
except Exception as e:
    print(f"❌ Connection Error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save-user', methods=['POST'])
def save_user():
    user = request.form.get('username')
    passw = request.form.get('password')
    
    # 'buffered=True' solves the "Unread result found" error
    cursor = db.cursor(buffered=True) 
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, passw))
    db.commit()
    cursor.close() 
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    user_val = request.form.get('username')
    pass_val = request.form.get('password')
    
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user_val, pass_val))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        # This sends the user to your shop after successful login
        return render_template('dashboard.html', username=user_val)
    else:
        return "Invalid login. <a href='/'>Try again</a>"

if __name__ == '__main__':
    app.run(debug=True, port=3000)

