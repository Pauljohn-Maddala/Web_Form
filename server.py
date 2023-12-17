from flask import Flask, request, jsonify, abort
from datetime import datetime
import uuid

app = Flask(__name__)


posts = {}

@app.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()
    user_key = data.get('user_key')

    # User authentication (update as per your actual authentication logic)
    if user_key != AUTH_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    post_id = str(uuid.uuid4())
    post = {
        'id': post_id,
        'msg': data.get('msg', ''),
        'timestamp': datetime.now().isoformat(),
    }
    posts[post_id] = post
    return jsonify(post), 200

@app.route('/post/<string:id>', methods=['GET'])
def read_post(id):
    post = posts.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
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
