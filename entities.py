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
from flask_login import UserMixin
from pony.orm import (
    composite_key,
    Database,
    Optional,
    PrimaryKey,
    Required,
    Set)
from uuid import (
    UUID,
    uuid4)


# database

db = Database()


# models

class User(UserMixin, db.Entity):
    """User entity. This serves double-duty as the user object for the authentication logic."""

    id = PrimaryKey(UUID, default=uuid4)
    """Unique identifier for the user."""

    name = Required(str, max_len=32, unique=True)
    """Login identifier/username."""

    bookmarks = Set('Bookmark')
    """Bookmarks relationship."""

    tags = Set('Tag')
    """Tag relationship."""


class Bookmark(db.Entity):
    """Bookmark entity."""

    id = PrimaryKey(UUID, default=uuid4)
    """Unique identifier for the bookmark."""

    label = Required(str, max_len=256)
    """Visible label for the bookmark."""

    url = Required(str, max_len=2048)
    """URL for the bookmark."""

    text = Optional(str, max_len=4096)
    """"""

    created = Required(datetime, precision=6)
    """Creation timestamp."""

    modified = Required(datetime, precision=6)
    """Last modification timestamp."""

    trashed = Required(bool, default=False)
    """Trashed status of the bookmark."""

    user = Required(User)
    """User relationship."""

    tags = Set('Tag')
    """Tags."""


class Tag(db.Entity):
    """Tag entity."""

    id = PrimaryKey(UUID, default=uuid4)
    """Unique identifier for the tag."""

    label = Required(str, max_len=32)
    """Visible label for the tag."""

    trashed = Required(bool, default=False)
    """Trashed status of the tag."""

    user = Required(User)
    """User relationship."""

    bookmarks = Set(Bookmark)
    """Bookmark relationship."""

    composite_key(label, user)
    """Uniqueness constraint on owning user and label."""
