from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import os
from werkzeug.security import check_password_hash

app = Flask(__name__)

USER_DATA_FILE = 'users.json'
DATA_FILE = 'data.txt'

if not os.path.exists(USER_DATA_FILE):
    default_users = [
        {
            'email': 'admin@gmail.com',
            'password': 'hashed_password_here'  
        }
    ]
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(default_users, f)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        f.write('[]')

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dash.html')

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        if data:
            print("Data received:", data)

            try:
                with open(DATA_FILE, 'r') as f:
                    current_data = json.load(f)
            except json.JSONDecodeError:
                current_data = []

            current_data.append(data)

            with open(DATA_FILE, 'w') as f:
                json.dump(current_data, f)

            return jsonify({"message": "Data received and saved successfully"}), 200
        else:
            return jsonify({"error": "No data received"}), 400
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        with open(DATA_FILE, 'r') as f:
            current_data = json.load(f)

        return jsonify(current_data), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(data)
        email = data.get('email')
        password = data.get('password')

        with open(USER_DATA_FILE, 'r') as f:
            users = json.load(f)

        user = next((user for user in users if user['email'] == email), None)

        if user and user['password'] ==password:
            return jsonify({"success": True, "message": "Login successful"}), 200
        else:
            return jsonify({"success": False, "message": "Invalid email or password"}), 401
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
    return 'Logged out successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
