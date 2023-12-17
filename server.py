from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from marshmallow import Schema, fields, validate
import logging
import secrets
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SECRET_KEY'] = 'your-secret-key'

# Extensions Initialization
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
logging.basicConfig(filename='server.log', level=logging.DEBUG)

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add additional fields as needed

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(500), nullable=False)
    key = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.String(25), nullable=False)

# Schema for Validation
class PostSchema(Schema):
    msg = fields.Str(required=True, validate=validate.Length(max=500))

post_schema = PostSchema()

# Initialize database
def initialize_database():
    with app.app_context():
        db.create_all()

@app.before_first_request
def create_tables():
    db.create_all()

# Routes
@app.route('/post', methods=['POST'])
def create_post():
    logging.info('Post request received')
    if not request.is_json:
        return "Invalid format, JSON required", 400

    errors = post_schema.validate(request.get_json())
    if errors:
        return jsonify(errors), 400

    data = request.get_json()
    key = secrets.token_urlsafe(16)
    timestamp = datetime.utcnow().isoformat() + "Z"
    new_post = Post(msg=data['msg'], key=key, timestamp=timestamp)
    db.session.add(new_post)
    db.session.commit()

    response = {'id': new_post.id, 'key': key, 'timestamp': timestamp}
    return jsonify(response), 201

@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return "Post not found", 404

    response = {
        'id': post_id,
        'timestamp': post.timestamp,
        'msg': post.msg
    }
    return jsonify(response)

@app.route('/post/<int:post_id>/delete/<key>', methods=['DELETE'])
def delete_post(post_id, key):
    post = Post.query.get(post_id)
    if post is None:
        return "Post not found", 404

    if post.key != key:
        return "Forbidden: Incorrect key", 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({'id': post_id, 'key': key, 'timestamp': post.timestamp})

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
