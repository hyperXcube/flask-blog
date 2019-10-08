from flask import Blueprint, redirect, url_for, request, render_template

from ..models import Post

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect(url_for('main.home'))

@bp.route('/home')
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.post_date.desc()) # Arranged in descending order
    return render_template('home.html', posts=posts.paginate(per_page=5, page=page))

@bp.route('/about')
def about():
    return render_template('about.html', title='About')

