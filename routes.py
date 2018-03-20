# Copyright 2018 Matthew Bishop
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from entities import User as UserEntity
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from forms import LoginForm
from main import application
from pony.orm import db_session
from werkzeug.security import check_password_hash, generate_password_hash


@application.route('/login', methods=['POST'])
def login():
    """User login processing."""

    form = LoginForm()

    # This is a one page site, we always redirect to the same place
    redirect_url = request.args.get('next') or url_for('index')
    redirect_response = redirect(redirect_url)

    if not form.validate_on_submit():
        # Form data failed validation, flash error messages to user
        for error in form.name.errors:
            flash('{}: {}'.format(form.name.label.text, error))
        for error in form.password.errors:
            flash('{}: {}'.format(form.password.label.text, error))

        return redirect_response

    with db_session:
        user = UserEntity.get(name=form.name.data)

        if not user:
            # HACK: User does not exist, register them
            password = generate_password_hash(form.password.data)
            user = UserEntity(name=form.name.data, password_hash=password, administrator=True)

            flash('{} registered'.format(user.name))

        elif not check_password_hash(user.password_hash, form.password.data):
            # User exists, password incorrect
            flash('Credentials incorrect')

            return redirect_response

        # User found, password correct, log 'em in
        login_user(user, remember=True)

        flash('{} logged on'.format(user.name))

    return redirect_response


@application.route('/logout')
def logout():
    """User logout."""

    logout_user()

    redirect_url = url_for('index')
    redirect_response = redirect(redirect_url)
    return redirect_response


@application.route('/')
def index():
    """Landing page."""

    login_form = LoginForm()
    urls = {
        'login': url_for('login'),
        'logout': url_for('logout')
    }

    output = render_template('index.html', login_form=login_form, urls=urls)
    return output
