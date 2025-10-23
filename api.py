from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated in-memory database
users = {}


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Returns user info by ID"""
    user = users.get(user_id)
    if user:
        return jsonify({"id": user_id, "name": user}), 200
    return jsonify({"error": "User not found"}), 404


@app.route('/users', methods=['POST'])
def add_user():
    """Adds a new user"""
    data = request.get_json()
    user_id = data.get("id")
    name = data.get("name")

    if not user_id or not name:
        return jsonify({"error": "Invalid data"}), 400

    if user_id in users:
        return jsonify({"error": "User already exists"}), 400

    users[user_id] = name
    return jsonify({"id": user_id, "name": name}), 201


if __name__ == '__main__':
    app.run(debug=True)
