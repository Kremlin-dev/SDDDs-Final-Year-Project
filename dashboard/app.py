from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# File path for storing data
DATA_FILE = 'data.txt'

# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        f.write('[]')
@app.route('/dashboard')
def dashboard():
    return render_template('dash.html')

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        if data:
            print("Data received:", data)

            # Read existing data from the file
            try:
                with open(DATA_FILE, 'r') as f:
                    current_data = json.load(f)
            except json.JSONDecodeError:
                current_data = []

            # Append the new data
            current_data.append(data)

            # Write the updated data back to the file
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
        # Read data from the file
        with open(DATA_FILE, 'r') as f:
            current_data = json.load(f)

        return jsonify(current_data), 200
    except Exception as e:
        print(f"Error occurred: {e}")
@app.route('/logout')
def logout():
    # Implement logout logic here
    return 'Logged out successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)