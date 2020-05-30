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


from entities import (
    User as UserEntity)
from flask import (
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for)
from flask_login import (
    login_user,
    logout_user)

from forms import (
    AddBookmarkForm,
    AddTagForm,
    LoginForm)
from main import app
from pony.orm import db_session
from rest import (
    BookmarkList as BookmarkListResource,
    TagList as TagListResource)


@app.route('/')
def index():
    """Landing page."""

    with db_session:
        context = {
            'forms': {
                'add_bookmark': AddBookmarkForm(),
                'add_tag': AddTagForm(),
                'login': LoginForm()},
            'messages': get_flashed_messages(),
            'urls': {
                'add_bookmark': url_for('bookmark_list'),
                'add_tag': url_for('tag_list'),
                'login': url_for('login'),
                'logout': url_for('logout')}}

        output = render_template('index.html', **context)
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
            flash('{form.name.label.text}: {error}')

        return redirect_response

    with db_session:
        user = UserEntity.get(name=form.name.data)

        if not user:
            # HACK: User does not exist, register them
            user = UserEntity(name=form.name.data)

            flash(f'{user.name} registered')

        # User found, password correct, log 'em in
        login_user(user, remember=True)

        flash(f'{user.name} logged on')

    return redirect_response


@app.route('/logout')
def logout():
    """User logout."""

    logout_user()

    redirect_url = url_for('index')
    redirect_response = redirect(redirect_url)
    return redirect_response
