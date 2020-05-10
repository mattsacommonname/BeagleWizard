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
from flask import abort
from flask_login import (
    current_user,
    login_required)
from flask_restful import Resource
from pony.orm import db_session
from pony.orm.core import ObjectNotFound
from uuid import UUID

from entities import (
    Bookmark as BookmarkEntity,
    Tag as TagEntity)
from forms import (
    AddBookmarkForm,
    AddTagForm)
from schemas import (
    Bookmark as BookmarkSchema,
    Tag as TagSchema)


class LoginRequiredResource(Resource):
    """Base class for REST resources so that they require a login."""

    method_decorators = [login_required]


class Bookmark(LoginRequiredResource):
    """Represents an individual bookmark REST resource."""

    def __init__(self):
        """Constructor."""

        super().__init__()
        self._schema = BookmarkSchema()

    def _get_bookmark(self, bookmark_id):
        """Gets a REST appropriate output formatted bookmark from an ID."""

        try:
            uuid = UUID(bookmark_id)
        except ValueError as ex:
            abort(400)

        try:
            bookmark = BookmarkEntity[uuid]
        except ObjectNotFound as ex:
            abort(404)

        output = self._schema.dump(bookmark)
        return output

    def get(self, bookmark_id):
        """Gets a bookmark."""

        with db_session:
            output = self._get_bookmark(bookmark_id)
            return output

    def patch(self, bookmark_id):
        """Partially updates a bookmark."""

        with db_session:
            output = self._get_bookmark(bookmark_id)
            return output

    def put(self, bookmark_id):
        """Updates a bookmark."""

        with db_session:
            output = self._get_bookmark(bookmark_id)
            return output


class BookmarkList(LoginRequiredResource):
    """Represents a list of bookmarks REST resource."""

    def __init__(self):
        """Constructor."""

        super().__init__()
        self._schema = BookmarkSchema()

    def get(self):
        """Gets the list of bookmarks."""

        with db_session:
            user = current_user.get_entity()
            bookmarks = [bookmark for bookmark in user.bookmarks]
            output = self._schema.dump(bookmarks, many=True)
            return output

    def post(self):
        """Creates a new bookmark."""

        form = AddBookmarkForm()
        if not form.validate_on_submit():
            abort(400)

        with db_session:
            user = current_user.get_entity()
            bookmark = BookmarkEntity(label=form.label.data, url=form.url.data, text=form.text.data,
                                      created=datetime.utcnow(), modified=datetime.utcnow(), user=user)

            output = self._schema.dump(bookmark)
            return output


class Tag(LoginRequiredResource):
    """Represents an individual tag REST resource."""

    def __init__(self):
        """Constructor."""

        super().__init__()
        self._schema = TagSchema()

    def _get_tag(self, tag_id):
        """Gets a REST appropriate output formatted tag from an ID."""

        try:
            uuid = UUID(tag_id)
        except ValueError as ex:
            abort(400)

        try:
            tag = TagEntity[uuid]
        except ObjectNotFound as ex:
            abort(404)

        output = self._schema.dump(tag)
        return output

    def get(self, tag_id):
        """Gets a tag."""

        with db_session:
            output = self._get_tag(tag_id)
            return output

    def put(self, tag_id):
        """Updates a tag."""

        with db_session:
            output = self._get_tag(tag_id)
            return output


class TagList(LoginRequiredResource):
    """Represents a list of tags REST resource."""

    def __init__(self):
        """Constructor."""

        super().__init__()
        self._schema = TagSchema()

    def get(self):
        """Gets the list of tags."""

        with db_session:
            user = current_user.get_entity()
            tags = list(user.tags)
            output = self._schema.dump(tags, many=True)
            return output

    def post(self):
        """Creates a new tag."""

        form = AddTagForm()
        if not form.validate_on_submit():
            abort(400)

        with db_session:
            user = current_user.get_entity()
            tag = TagEntity(label=form.label.data, user=user)

            output = self._schema.dump(tag)
            return output
