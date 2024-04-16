from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Priorauth
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import openai
import os


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        password = request.form.get('password')
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)

            priorauth_data = Priorauth.query.all()
                       
            return render_template('payor1.html', priorauth_data=priorauth_data)
            #return render_template("payor.html", user=current_user)

            #return redirect(url_for('views.receive_prior_auth_request'))
        else:
            flash('Incorrect password, try again.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

