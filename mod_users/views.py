from flask import render_template, request, flash, redirect, url_for
from mod_users.forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
from . import users
from mod_users import User
from app import db


@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('users/register.html', form=form)
        if not form.password.data == form.confirm_password.data:
            flash('Password and Confirm Password does not match', category='error')
            return render_template('users/register.html', form=form)
        new_user = User()
        new_user.name = form.name.data
        new_user.email = form.email.data
        new_user.set_password(form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully')
            return render_template('users/register.html', form=form)
        except IntegrityError:
            db.session.rollback()
            flash('This Email already used')
            render_template('users/register.html', form=form)
    return render_template('users/register.html', form=form)


@users.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('users/login.html', form=form)
        user = User.query.filter(User.email == form.email.data).first()
        if not user:
            flash('User does\'nt exist!')
            return render_template('users/login.html', form=form)
        if not user.check_password(form.password.data):
            flash('Your password is wrong!')
            return render_template('users/login.html', form=form)
        return render_template('users/index.html')
    return render_template('users/login.html', form=form)


@users.route('/logout/')
def logout():
    flash('You logged out successfully')
    return redirect(url_for('users.login'))