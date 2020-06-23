from flask import render_template, request, flash, session, redirect, url_for
from . import admin
from app import db
from mod_users.forms import LoginForm
from mod_users.models import User


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
