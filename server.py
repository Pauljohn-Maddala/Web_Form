from flask import Flask, request, jsonify, abort
import uuid

app = Flask(__name__)

# Define a dictionary to store posts
posts = {}

@app.route('/post', methods=['POST'])
def create_post():
    # Get data from the request
    data = request.get_json()
    
    # Check if 'msg' field is present in the request
    if 'msg' not in data:
        return jsonify({"error": "'msg' field is required"}), 400
    
    # Generate a unique ID for the post
    post_id = str(uuid.uuid4())
    
    # Create the post dictionary
    post = {
        'id': post_id,
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
    
    # Return the post
    return jsonify(post), 200

@app.route('/post/<string:id>/delete/<string:key>', methods=['DELETE'])
def delete_post(id, key):
    # Check if the post exists
    if id not in posts:
        return jsonify({"error": "Post not found"}), 404
    
    # Check if the provided key matches the key in the post
    if key != posts[id]['key']:
        return jsonify({"error": "Unauthorized"}), 403
    
    # Delete the post
    del posts[id]
    
    return jsonify({"message": "Post deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
