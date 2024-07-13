from flask import Flask, request, jsonify

app = Flask(__name__)

data_store = []

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        print(data)
        if data:
            data_store.append(data)
            print("Data received:", data)
            return jsonify({"message": "Data received successfully"}), 200
        else:
            return jsonify({"error": "No data received"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/api/data', methods=['GET'])
# def get_all_data():
#     return jsonify(data_store), 200

if __name__ == '__main__':
    app.run(debug=True)
