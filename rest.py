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
from flask import (
    abort,
    request)
from flask_login import (
    current_user,
    login_required)
from flask_restful import Resource
from pony.orm import (
    db_session,
    desc,
    ObjectNotFound)
from pony.orm.core import ObjectNotFound
from typing import Callable
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

    _LIMIT_DEFAULT: int = 200
    _LIMIT_KEY: str = 'l'
    _LIMIT_MAX: int = 1000
    _LIMIT_MIN: int = 1

    _OFFSET_DEFAULT: int = 0
    _OFFSET_KEY: str = 'o'
    _OFFSET_MIN: int = 0

    _SORT_DEFAULT: str = BookmarkEntity.modified.name
    _SORT_KEY: str = 's'
    _SORT_REVERSE_INDICATOR: str = '-'

    _TAG_KEY: str = 't'

    _schema: BookmarkSchema = BookmarkSchema()

    _sortable_fields: list = [
        BookmarkEntity.created,
        BookmarkEntity.label,
        BookmarkEntity.modified,
        BookmarkEntity.url]

    _name_field_map: dict = {field.name: field for field in _sortable_fields}

    @staticmethod
    def _order_by(field_name: str):
        """Builds the value to order the bookmark list query by.

        :param field_name: Name of the field to sort on.

        :return: A valid sortable value.
        """

        if field_name is None:
            raise ValueError('field_name cannot be None')

        descending = field_name.startswith(BookmarkList._SORT_REVERSE_INDICATOR)
        name = field_name.strip(BookmarkList._SORT_REVERSE_INDICATOR)
        field = BookmarkList._name_field_map.get(name, None)
        if field is None:  # not a valid field to order by
            raise ValueError(f'"{field_name}" is not a valid field to sort by')

        if descending:
            return desc(field)
        return field

    @staticmethod
    def _selector(tag: TagEntity) -> Callable:
        """Build selection filter for bookmark list query.

        :param tag: The tag id attached to filter on.

        :return: The selector function.
        """

        if tag is None:
            return lambda bookmark: True

        return lambda bookmark: tag in bookmark.tags

    @staticmethod
    def get():
        f"""Gets the list of bookmarks.
        
        URL query keys:
        
        - {BookmarkList._OFFSET_KEY}: Offset to begin at. Value must be non-negative. Defaults to
          {BookmarkList._OFFSET_DEFAULT}.
        - {BookmarkList._LIMIT_KEY}: Maximum number of results to return. Value must be positive. Defaults to
          {BookmarkList._LIMIT_DEFAULT}
        - {BookmarkList._SORT_KEY}: Field to sort on. Must be a value in
          {BookmarkList._name_field_map.keys()}. Can be prefixed with {BookmarkList._SORT_REVERSE_INDICATOR} to reverse
          the order. Defaults to {BookmarkList._SORT_DEFAULT}
        - {BookmarkList._TAG_KEY}: ID of a tag to filter on."""

        try:
            offset = int(request.args.get(BookmarkList._OFFSET_KEY, BookmarkList._OFFSET_DEFAULT))
            if offset < BookmarkList._OFFSET_MIN:
                raise ValueError(f'offset of "{offset}" less than minimum "{BookmarkList._OFFSET_MIN}"')
        except (TypeError, ValueError) as ex:
            abort(400)

        try:
            limit = int(request.args.get(BookmarkList._LIMIT_KEY, BookmarkList._LIMIT_DEFAULT))
            if limit < BookmarkList._LIMIT_MIN:
                raise ValueError(f'limit of "{limit}" is less than minimum "{BookmarkList._LIMIT_MIN}"')
            if limit > BookmarkList._LIMIT_MAX:
                raise ValueError(f'limit of "{limit}" is greater than maximum "{BookmarkList._LIMIT_MAX}"')
        except (TypeError, ValueError) as ex:
            abort(400)

        end = offset + limit

        tag_id = request.args.get(BookmarkList._TAG_KEY, None)
        try:
            tag_uuid = UUID(tag_id) if tag_id else None
        except (AttributeError, TypeError, ValueError) as ex:
            abort(400)

        with db_session:
            try:
                tag = TagEntity[tag_uuid] if tag_uuid else None
            except ObjectNotFound as ex:
                abort(400)

            selector = BookmarkList._selector(tag)

            sort = request.args.get(BookmarkList._SORT_KEY, BookmarkList._SORT_DEFAULT)

            try:
                order_by = BookmarkList._order_by(sort)
            except ValueError as ex:
                abort(400)

            user = current_user.get_entity()
            bookmarks = [bookmark for bookmark in user.bookmarks.select(selector).order_by(order_by)[offset:end]]
            output = BookmarkList._schema.dump(bookmarks, many=True)
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

            output = BookmarkList._schema.dump(bookmark)
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
