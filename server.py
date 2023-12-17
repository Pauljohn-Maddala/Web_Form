from flask import Flask, request, jsonify, abort
import uuid

app = Flask(__name__)

# Define dictionaries to store posts and users
posts = {}
users = {}

@app.route('/user', methods=['POST'])
def create_user():
    # Generate a unique user ID
    user_id = str(uuid.uuid4())

    # Generate a unique user key
    user_key = str(uuid.uuid4())

    # Create the user dictionary
    user = {
        'id': user_id,
        'key': user_key,
    }

    # Store the user in the dictionary
    users[user_id] = user

    return jsonify(user), 200

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
    if user_id not in users or user_key != users[user_id]['key']:
        return jsonify({"error": "Unauthorized"}), 403
    
    # Generate a unique ID for the post
    post_id = str(uuid.uuid4())
    
    # Create the post dictionary
    post = {
        'id': post_id,
        'msg': data['msg'],
        'timestamp': str(uuid.uuid4()),  # For testing purposes, generate a timestamp
        'user_id': user_id,
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
    
    # Include the associated user ID in the response
    post['user_id'] = post['user_id']
    
    return jsonify(post), 200

@app.route('/post/<string:id>/delete', methods=['DELETE'])
def delete_post(id):
    # Check if the post exists
    if id not in posts:
        return jsonify({"error": "Post not found"}), 404
    
    # Get data from the request
    data = request.get_json()

    # Check if 'user_key' field is present in the request
    if 'user_key' not in data:
        return jsonify({"error": "'user_key' field is required"}), 400

    # Check if the provided user key matches the user's key
    user_key = data['user_key']
    post = posts[id]
    user_id = post['user_id']
    
    if user_key != users[user_id]['key']:
        return jsonify({"error": "Unauthorized"}), 403
    
    # Delete the post
    del posts[id]
    
    return jsonify({"message": "Post deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
