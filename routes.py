# Copyright 2020 Matthew Bishop
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


from datetime import datetime
from entities import (
    Bookmark as BookmarkEntity,
    User as UserEntity)
from flask import (
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for)
from flask_login import (
    current_user,
    login_user,
    logout_user)
from forms import (
    AddBookmarkForm,
    LoginForm)
from main import app
from pony.orm import (
    db_session,
    select)


@app.route('/addbookmark', methods=['POST'])
def add_bookmark():
    form = AddBookmarkForm()

    redirect_url = url_for('index')
    redirect_response = redirect(redirect_url)

    if not form.validate_on_submit():
        for error in form.label.errors:
            flash('{}: {}'.format(form.label.label.text, error))
        for error in form.url.errors:
            flash('{}: {}'.format(form.url.label.text, error))

        return redirect_response

    with db_session:
        user_entity = current_user.get_entity()
        bookmark = BookmarkEntity(label=form.label.data, url=form.url.data, text=form.text.data,
                                  created=datetime.utcnow(), modified=datetime.utcnow(), user=user_entity)

        flash('Added bookmark "{}"'.format(bookmark.label))

    return redirect_response


def get_bookmarks(user):
    if user is None or not user.is_authenticated:
        return None

    user_entity = user.get_entity()
    bookmarks = select(b for b in BookmarkEntity if b.user == user_entity)

    return bookmarks


@app.route('/')
def index():
    """Landing page."""

    add_bookmark_form = AddBookmarkForm()
    login_form = LoginForm()
    urls = {
        'addbookmark': url_for('addbookmark'),
        'login': url_for('login'),
        'logout': url_for('logout')
    }
    messages = get_flashed_messages()
    with db_session:
        bookmarks = get_bookmarks(current_user)

        output = render_template('index.html', add_bookmark_form=add_bookmark_form, bookmarks=bookmarks,
                                 login_form=login_form, messages=messages, urls=urls)
    return output


@app.route('/login', methods=['POST'])
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

        return redirect_response

    with db_session:
        user = UserEntity.get(name=form.name.data)

        if not user:
            # HACK: User does not exist, register them
            user = UserEntity(name=form.name.data)

            flash('{} registered'.format(user.name))

        # User found, password correct, log 'em in
        login_user(user, remember=True)

        flash('{} logged on'.format(user.name))

    return redirect_response


@app.route('/logout')
def logout():
    """User logout."""

    logout_user()

    redirect_url = url_for('index')
    redirect_response = redirect(redirect_url)
    return redirect_response
