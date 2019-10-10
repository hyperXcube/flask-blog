import os

from flask import Blueprint, current_app, redirect, url_for, flash, render_template, request
from flask_login import login_required, login_user, logout_user, current_user

from .. import db, bcrypt
from ..models import User, Post
from .forms import RegisterForm, LoginForm, UpdateAccountForm, RequestPasswordResetForm, PasswordResetForm
from .utils import send_pw_reset_email, save_profile_pic

bp = Blueprint('users', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.home'))
        flash('Login unsuccessful. Check username or password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route('/reset_password', methods=['GET', 'POST'])
def request_pw_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_pw_reset_email(user)
        flash('An email has been send with password reset instructions.', 'success')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', title='Reset Password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def pw_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_pw_reset_token(token)
    if not user:
        flash('That is an invalid or expired token.', 'danger')
        return redirect(url_for('users.request_pw_reset'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data)
        user.password = password_hash
        db.session.commit()
        flash('Password successfully changed! You can now log in with your new password.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_pw.html', title='Reset Password', form=form)

@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.profile_pic.data:
            if current_user.profile_pic != 'default.jpg':
                os.remove(os.path.join(current_app.root_path, 'static', current_user.profile_pic))
            current_user.profile_pic = save_profile_pic(form.profile_pic.data)
        db.session.commit()
        flash('Account info updated.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for('static', filename=current_user.profile_pic)
    return render_template('account.html', title='Account', img_file=img_file, form=form)

@bp.route('/user/<username>')
def user(username):
    page = request.args.get('page', default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.post_date.desc())
    return render_template('user.html', title=username, posts=posts.paginate(per_page=5, page=page), user=user)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('main.home'))
