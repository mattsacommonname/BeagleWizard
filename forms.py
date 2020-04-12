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

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField)
from wtforms.validators import (
    DataRequired,
    Length)


class AddBookmarkForm(FlaskForm):
    """Add bookmark form."""

    label = StringField('Label', validators=[DataRequired(), Length(min=1, max=256)])
    """Bookmark label."""

    url = StringField('URL', validators=[DataRequired(), Length(min=3, max=2048)])
    """Bookmark URL."""

    text = StringField('Text', validators=[Length(max=4096)])
    """Text/noted for the bookmark."""

    submit = SubmitField('Add')


class LoginForm(FlaskForm):
    """User login form."""

    name = StringField('User name', validators=[DataRequired(), Length(min=3, max=32)])
    """User name."""

    submit = SubmitField('Login')
    """Submit button."""
