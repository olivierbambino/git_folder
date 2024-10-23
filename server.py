from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/art_gallery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('artworks', lazy=True))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
    artwork = db.relationship('Artwork', backref=db.backref('feedbacks', lazy=True))

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('blog_posts', lazy=True))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/artworks', methods=['POST'])
def upload_artwork():
    data = request.get_json()
    title = data['title']
    description = data['description']
    image = data['image']
    category = data['category']
    user_id = data['user_id']
    new_artwork = Artwork(title=title, description=description, image=image, category=category, user_id=user_id)
    db.session.add(new_artwork)
    db.session.commit()
    return jsonify({'message': 'Artwork uploaded successfully'}), 201

@app.route('/api/artworks', methods=['GET'])
def get_artworks():
    artworks = Artwork.query.all()
    artworks_list = []
    for artwork in artworks:
        artworks_list.append({
            'id': artwork.id,
            'title': artwork.title,
            'description': artwork.description,
            'image': artwork.image,
            'category': artwork.category,
            'user_id': artwork.user_id
        })
    return jsonify(artworks_list), 200

@app.route('/api/feedback', methods=['POST'])
def leave_feedback():
    data = request.get_json()
    content = data['content']
    user_id = data['user_id']
    artwork_id = data['artwork_id']
    new_feedback = Feedback(content=content, user_id=user_id, artwork_id=artwork_id)
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback submitted successfully'}), 201

@app.route('/api/blog-posts', methods=['POST'])
def create_blog_post():
    data = request.get_json()
    title = data['title']
    content = data['content']
    user_id = data['user_id']
    new_blog_post = BlogPost(title=title, content=content, user_id=user_id)
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({'message': 'Blog post created successfully'}), 201

@app.route('/api/blog-posts', methods=['GET'])
def get_blog_posts():
    blog_posts = BlogPost.query.all()
    blog_posts_list = []
    for post in blog_posts:
        blog_posts_list.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'user_id': post.user_id
        })
    return jsonify(blog_posts_list), 200

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    title = data['title']
    description = data['description']
    date = data['date']
    new_event = Event(title=title, description=description, date=date)
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully'}), 201

@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = []
    for event in events:
        events_list.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date
        })
    return jsonify(events_list), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
