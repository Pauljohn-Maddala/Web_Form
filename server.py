from flask import Flask, request, jsonify
import secrets
from datetime import datetime

app = Flask(__name__)

posts = {}
next_id = 1
users = {}
next_user_id = 1  # Initialize next_user_id

@app.route('/user', methods=['POST'])
def create_user():
    global next_user_id
    user_id = str(next_user_id)
    user_key = secrets.token_urlsafe(16)
    users[user_id] = {'user_key': user_key}
    next_user_id += 1
    return jsonify({'user_id': user_id, 'user_key': user_key})

@app.route('/post', methods=['POST'])
def create_post():
    global next_id
    if not request.is_json:
        return "Invalid format, JSON required", 400

    data = request.get_json()
    if 'msg' not in data or not isinstance(data['msg'], str) or 'user_id' not in data or 'user_key' not in data:
        return "Bad request: 'msg', 'user_id', and 'user_key' fields are required", 400

    user_id = data['user_id']
    user_key = data['user_key']

    if user_id not in users or users[user_id]['user_key'] != user_key:
        return jsonify({'error': 'Invalid user ID or key'}), 403

    key = secrets.token_urlsafe(16)
    timestamp = datetime.utcnow().isoformat() + "Z"
    posts[next_id] = {'msg': data['msg'], 'key': key, 'timestamp': timestamp, 'user_id': user_id}

    response = {'id': next_id, 'key': key, 'timestamp': timestamp, 'user_id': user_id}
    next_id += 1
    return jsonify(response)

@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    post = posts.get(post_id)
    if post is None:
        return "Post not found", 404

    response = {
        'id': post_id,
        'timestamp': post['timestamp'],
        'msg': post['msg']
    }
    return jsonify(response)

@app.route('/post/<int:post_id>/delete/<key>', methods=['DELETE'])
def delete_post(post_id, key):
    post = posts.get(post_id)
    if post is None:
        return "Post not found", 404

    user_id = post.get('user_id')
    if key != post['key'] and (not user_id or key != users[user_id]['user_key']):
        return "Forbidden: Incorrect key", 403

    del posts[post_id]
    return jsonify({'message': 'Post deleted'})

@app.route('/posts/range', methods=['GET'])
def get_posts_in_range():
    start = request.args.get('start')
    end = request.args.get('end')
    
    start_dt = datetime.fromisoformat(start) if start else None
    end_dt = datetime.fromisoformat(end) if end else None

    filtered_posts = {id: post for id, post in posts.items() if 
                      (not start_dt or datetime.fromisoformat(post['timestamp']) >= start_dt) and
                      (not end_dt or datetime.fromisoformat(post['timestamp']) <= end_dt)}

    return jsonify(filtered_posts)

@app.route('/posts/user/<user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    user_posts = {id: post for id, post in posts.items() if post.get('user_id') == user_id}
    return jsonify(user_posts)

if __name__ == '__main__':
    app.run(debug=True)
