from flask import Flask, request, jsonify, abort
from datetime import datetime
import uuid

app = Flask(__name__)

# Dictionary to store posts and users
posts = {}
users = {}

# Function to generate a current timestamp
def current_timestamp():
    return datetime.now().isoformat()

@app.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()

    # Validate request data
    if 'msg' not in data:
        return jsonify({"error": "'msg' field is required"}), 400
    if 'user_id' not in data or 'user_key' not in data:
        return jsonify({"error": "'user_id' and 'user_key' fields are required"}), 400

    user_id = data['user_id']
    user_key = data['user_key']

    # User authentication
    if user_id not in users or users[user_id] != user_key:
        return jsonify({"error": "Unauthorized"}), 403

    post_id = str(uuid.uuid4())
    post = {
        'id': post_id,
        'user_id': user_id,
        'msg': data['msg'],
        'timestamp': current_timestamp(),
    }
    posts[post_id] = post
    return jsonify(post), 200

@app.route('/post/<string:id>', methods=['GET'])
def read_post(id):
    if id not in posts:
        return jsonify({"error": "Post not found"}), 404

    post = posts[id]
    return jsonify(post), 200

@app.route('/post/<string:id>/delete/<string:key>', methods=['DELETE'])
def delete_post(id, key):
    if id not in posts:
        return jsonify({"error": "Post not found"}), 404

    if key != posts[id]['user_id']:
        return jsonify({"error": "Unauthorized"}), 403

    del posts[id]
    return jsonify({"message": "Post deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
