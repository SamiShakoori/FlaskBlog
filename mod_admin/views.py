from flask import render_template, request, flash, session, redirect, url_for
from sqlalchemy.exc import IntegrityError
from . import admin
from app import db
from mod_users.forms import LoginForm, RegisterForm
from mod_users.models import User
from mod_blog.forms import CreatePostForm
from mod_blog.models import Post


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/login.html', form=form)
        user = User.query.filter(User.email == form.email.data).first()
        if not user:
            flash('User does\'nt exist!', category='error')
            return render_template('admin/login.html', form=form)
        if not user.check_password(form.password.data):
            flash('Your password is wrong!', category='error')
            return render_template('admin/login.html', form=form)
        if not user.is_admin():
            flash('Incorrect Credential', category='error')
            return render_template('admin/login.html', form=form)
        session['email'] = user.email
        session['user_id'] = user.id
        session['role'] = user.role
        return render_template('admin/index.html')
        # return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout/')
def logout():
    session.clear()
    flash('You logged out successfully', category='error')
    return redirect(url_for('admin.login'))


@admin.route('/users/', methods=['GET', 'POST'])
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin/list_users.html', users=users)


@admin.route('/users/delete/<int:user_id>/')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User delete successfully!')
    return redirect(url_for('admin.list_users'))


@admin.route('/user/new/', methods=['GET', 'POST'])
def create_user():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/create_user.html', form=form)
        if not form.password.data == form.confirm_password.data:
            flash('Password and Confirm Password does not match', category='error')
            return render_template('admin/create_user.html', form=form)
        new_user = User()
        new_user.name = form.name.data
        new_user.email = form.email.data
        new_user.set_password(form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('New user added successfully.')
            return render_template('admin/create_user.html', form=form)
        except IntegrityError:
            db.session.rollback()
            flash('This email had already used!')
            return render_template('admin/create_user.html', form=form)
    return render_template('admin/create_user.html', form=form)


@admin.route('/posts/new/', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/create_post.html', form=form)
        new_post = Post()
        new_post.title = form.title.data
        new_post.slug = form.slug.data
        new_post.content = form.content.data
        new_post.summary = form.summary.data
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post created.')
            return render_template('admin/create_post.html', form=form)
        except IntegrityError:
            db.session.rollback()
            flash('Try Again!')
            return render_template('admin/create_post.html', form=form)
    return render_template('admin/create_post.html', form=form)


@admin.route('/posts/')
def list_post():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('admin/list_post.html', posts=posts)


@admin.route('/posts/delete/<int:post_id>/')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.')
    return redirect(url_for('admin.list_post'))
