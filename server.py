from flask import Flask, request, jsonify
import secrets
from datetime import datetime

app = Flask(__name__)

# Initialize posts as an empty dictionary
posts = {}
next_id = 1
data_file = "posts.json"  # File to store posts

# Function to save posts to the file
def save_posts():
    try:
        with open(data_file, "w") as file:
            json.dump(posts, file)
    except Exception as e:
        print(f"Error saving posts: {str(e)}")

# Function to load posts from the file
def load_posts():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading posts: {str(e)}")
        return {}

# Load posts from the file on server startup
posts = load_posts()

@app.route('/post', methods=['POST'])
def create_post():
    global next_id
    if not request.is_json:
        return "Invalid format, JSON required", 400

    data = request.get_json()
    if 'msg' not in data or not isinstance(data['msg'], str):
        return "Bad request: 'msg' field missing or not a string", 400

    user_id = data.get('user_id')
    user_key = data.get('user_key')

    if user_id and user_key:
        if user_id not in users or users[user_id].user_key != user_key:
            return jsonify({'error': 'Invalid user ID or key'}), 403

    key = secrets.token_urlsafe(16)
    timestamp = datetime.utcnow().isoformat() + "Z"
    posts[next_id] = {'msg': data['msg'], 'key': key, 'timestamp': timestamp}
    
    response = {'id': next_id, 'key': key, 'timestamp': timestamp}
    next_id += 1

    # Save posts to the file after creating a new post
    save_posts()
    
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
    if key != post['key'] and (not user_id or key != users[user_id].user_key):
        return "Forbidden: Incorrect key", 403

    del posts[post_id]
    save_posts()
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
