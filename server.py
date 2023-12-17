from flask import Flask, request, jsonify, abort
import uuid

app = Flask(__name__)

# Define dictionaries to store posts and users
posts = {}
users = {}

@app.route('/post', methods=['POST'])
def create_post():
    # Get data from the request
    data = request.get_json()
    
    # Check if 'msg', 'user_id', and 'user_key' fields are present in the request
    if 'msg' not in data or 'user_id' not in data or 'user_key' not in data:
        return jsonify({"error": "'msg', 'user_id', and 'user_key' fields are required"}), 400

    # Check if the user exists
    user_id = data['user_id']
    user_key = data['user_key']
    if user_id not in users or users[user_id] != user_key:
        return jsonify({"error": "Unauthorized"}), 403
    
    # Generate a unique ID for the post
    post_id = str(uuid.uuid4())
    
    # Create the post dictionary
    post = {
        'id': post_id,
        'user_id': user_id,
        'msg': data['msg'],
        'timestamp': str(uuid.uuid4()),  # For testing purposes, generate a timestamp
        'key': '',  # Initialize key as an empty string
    }
    
    # Store the post in the dictionary
    posts[post_id] = post
    
    return jsonify(post), 200

@app.route('/post/<string:id>', methods=['GET'])
def read_post(id):
    # Check if the post exists
    if id not in posts:
        return jsonify({"error": "Post not found"}), 404
    
    # Get the post
    post = posts[id]
    
    # Include the associated user_id
    post['user_id'] = users[post['user_id']]
    
    # Return the post
    return jsonify(post), 200

@app.route('/post/<string:id>/delete/<string:key>', methods=['DELETE'])
def delete_post(id, key):
    # Check if the post exists
    if id not in posts:
        return jsonify({"error": "Post not found"}), 404
    
    # Check if the provided key matches the key in the post or user's key
    if key != posts[id]['key'] and key != users[posts[id]['user_id']]:
        return jsonify({"error": "Unauthorized"}), 403
    
    # Delete the post
    del posts[id]
    
    return jsonify({"message": "Post deleted"}), 200

@app.route('/user', methods=['POST'])
def create_user():
    # Get data from the request
    data = request.get_json()

    # Check if 'user_id' and 'user_key' fields are present in the request
    if 'user_id' not in data or 'user_key' not in data:
        return jsonify({"error": "'user_id' and 'user_key' fields are required"}), 400

    # Check if the user already exists
    user_id = data['user_id']
    if user_id in users:
        return jsonify({"error": "User already exists"}), 400

    # Create the user
    users[user_id] = data['user_key']

    return jsonify({"message": "User created"}), 200

if __name__ == '__main__':
    app.run(debug=True)
