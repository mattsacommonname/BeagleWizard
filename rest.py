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
from flask_restful import (
    fields,
    marshal,
    Resource)
from pony.orm import db_session
from pony.orm.core import ObjectNotFound
from uuid import UUID

from entities import (
    Bookmark as BookmarkEntity,
    Tag as TagEntity)
from forms import (
    AddBookmarkForm,
    AddTagForm)


class LoginRequiredResource(Resource):
    """Base class for REST resources so that they require a login."""

    method_decorators = [login_required]


tag_fields = {
    'id': fields.String(attribute=lambda entity: str(entity.id)),
    'label': fields.String
}


bookmark_fields = {
    'id': fields.String(attribute=lambda entity: str(entity.id)),
    'label': fields.String,
    'tags': fields.List(fields.Nested(tag_fields)),
    'text': fields.String,
    'url': fields.String
}


class Bookmark(LoginRequiredResource):
    """Represents an individual bookmark REST resource."""

    @staticmethod
    def _get_bookmark(bookmark_id):
        """Gets a REST appropriate output formatted bookmark from an ID."""

        try:
            uuid = UUID(bookmark_id)
        except ValueError as ex:
            abort(400)

        try:
            bookmark = BookmarkEntity[uuid]
        except ObjectNotFound as ex:
            abort(404)

        output = marshal(bookmark, bookmark_fields)
        return output

    @staticmethod
    def get(bookmark_id):
        """Gets a bookmark."""

        with db_session:
            output = Bookmark._get_bookmark(bookmark_id)
            return output

    @staticmethod
    def patch(bookmark_id):
        """Partially updates a bookmark."""

        with db_session:
            output = Bookmark._get_bookmark(bookmark_id)
            return output

    @staticmethod
    def put(bookmark_id):
        """Updates a bookmark."""

        with db_session:
            output = Bookmark._get_bookmark(bookmark_id)
            return output


class BookmarkList(LoginRequiredResource):
    """Represents a list of bookmarks REST resource."""

    @staticmethod
    def get():
        """Gets the list of bookmarks."""

        with db_session:
            user = current_user.get_entity()
            bookmarks = list(user.bookmarks)
            output = marshal(bookmarks, bookmark_fields)
            return output

    @staticmethod
    def post():
        """Creates a new bookmark."""

        form = AddBookmarkForm()
        if not form.validate_on_submit():
            abort(400)

        with db_session:
            user = current_user.get_entity()
            bookmark = BookmarkEntity(label=form.label.data, url=form.url.data, text=form.text.data,
                                      created=datetime.utcnow(), modified=datetime.utcnow(), user=user)

            output = marshal(bookmark, bookmark_fields)
            return output


class Tag(LoginRequiredResource):
    """Represents an individual tag REST resource."""

    @staticmethod
    def _get_tag(tag_id):
        """Gets a REST appropriate output formatted tag from an ID."""

        try:
            uuid = UUID(tag_id)
        except ValueError as ex:
            abort(400)

        try:
            tag = TagEntity[uuid]
        except ObjectNotFound as ex:
            abort(404)

        output = marshal(tag, tag_fields)
        return output

    @staticmethod
    def get(tag_id):
        """Gets a tag."""

        with db_session:
            output = Tag._get_tag(tag_id)
            return output

    @staticmethod
    def put(tag_id):
        """Updates a tag."""

        with db_session:
            output = Tag._get_tag(tag_id)
            return output


class TagList(LoginRequiredResource):
    """Represents a list of tags REST resource."""

    @staticmethod
    def get():
        """Gets the list of tags."""

        with db_session:
            user = current_user.get_entity()
            tags = list(user.tags)
            output = marshal(tags, tag_fields)
            return output

    @staticmethod
    def post():
        """Creates a new tag."""

        form = AddTagForm()
        if not form.validate_on_submit():
            abort(400)

        with db_session:
            user = current_user.get_entity()
            tag = TagEntity(label=form.label.data, user=user)

            output = marshal(tag, tag_fields)
            return output
