from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///redaws.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    votes = db.Column(db.Integer, default=0)

# Create the database tables (run once)
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()  # show newest posts first
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/vote/<int:post_id>/<action>')
def vote(post_id, action):
    post = Post.query.get_or_404(post_id)
    if action == 'up':
        post.votes += 1
    elif action == 'down':
        post.votes -= 1
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
