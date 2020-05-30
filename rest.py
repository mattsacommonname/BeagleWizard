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
    request,
    Response)
from flask.views import MethodView
from flask_login import (
    current_user,
    login_required)
from functools import wraps
from marshmallow import ValidationError
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


def make_json_response(func):
    """Decorator to that will turn non Response results into Response object with an 'applicatoin/json' mime type.

    :param func: The function to decorate.

    :return: The decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, Response):
            return result

        return Response(result, 200, mimetype='application/json')

    return wrapper


class RestResource(MethodView):
    """Base class for REST resources so that they require a login."""

    decorators = [make_json_response, login_required]


class Bookmark(RestResource):
    """Represents an individual bookmark REST resource."""

    _schema = BookmarkSchema()

    @classmethod
    def _get_bookmark(cls, bookmark_id):
        """Gets a REST appropriate output formatted bookmark from an ID."""

        try:
            uuid = UUID(bookmark_id)
        except ValueError as ex:
            abort(400)

        try:
            bookmark = BookmarkEntity[uuid]
        except ObjectNotFound as ex:
            abort(404)

        output = cls._schema.dumps(bookmark)
        return output

    @classmethod
    def delete(cls, bookmark_id):
        """Deletes a bookmark.

        :param bookmark_id: ID of the bookmark to delete.

        :return: An HTTP response:
                 - If the delete was successful: 200 and a JSON representation of the deleted bookmark.
                 - If bookmark_id was invalid (i.e. not a valid UUID): 400
                 - If the bookmark didn't exist: 404
        """

        try:
            uuid = UUID(bookmark_id)
        except ValueError as ex:
            abort(400)

        with db_session:
            try:
                bookmark = BookmarkEntity[uuid]
            except ObjectNotFound as ex:
                abort(404)

            output = cls._schema.dumps(bookmark)

            bookmark.delete()

            return output

    @classmethod
    def get(cls, bookmark_id):
        """Gets a bookmark."""

        with db_session:
            output = cls._get_bookmark(bookmark_id)
            return output

    @classmethod
    def patch(cls, bookmark_id):
        """Partially updates a bookmark."""

        abort(501)

    @classmethod
    def put(cls, bookmark_id):
        """Updates a bookmark."""

        abort(501)


class BookmarkList(RestResource):
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

    @classmethod
    def _order_by(cls, field_name: str):
        """Builds the value to order the bookmark list query by.

        :param field_name: Name of the field to sort on.

        :return: A valid sortable value.
        """

        if field_name is None:
            raise ValueError('field_name cannot be None')

        descending = field_name.startswith(cls._SORT_REVERSE_INDICATOR)
        name = field_name.strip(cls._SORT_REVERSE_INDICATOR)
        field = cls._name_field_map.get(name, None)
        if field is None:  # not a valid field to order by
            raise ValueError(f'"{field_name}" is not a valid field to sort by')

        if descending:
            return desc(field)
        return field

    @classmethod
    def _selector(cls, tag: TagEntity) -> Callable:
        """Build selection filter for bookmark list query.

        :param tag: The tag id attached to filter on.

        :return: The selector function.
        """

        if tag is None:
            return lambda bookmark: True

        return lambda bookmark: tag in bookmark.tags

    @classmethod
    def get(cls):
        f"""Gets the list of bookmarks.
        
        URL query keys:
        
        - {cls._OFFSET_KEY}: Offset to begin at. Value must be non-negative. Defaults to {cls._OFFSET_DEFAULT}.
        - {cls._LIMIT_KEY}: Maximum number of results to return. Value must be positive. Defaults to
          {cls._LIMIT_DEFAULT}
        - {cls._SORT_KEY}: Field to sort on. Must be a value in {cls._name_field_map.keys()}. Can be prefixed with
          {cls._SORT_REVERSE_INDICATOR} to reverse the order. Defaults to {cls._SORT_DEFAULT}
        - {cls._TAG_KEY}: ID of a tag to filter on.
        """

        try:
            offset = int(request.args.get(cls._OFFSET_KEY, cls._OFFSET_DEFAULT))
            if offset < cls._OFFSET_MIN:
                raise ValueError(f'offset of "{offset}" less than minimum "{cls._OFFSET_MIN}"')
        except (TypeError, ValueError) as ex:
            abort(400)

        try:
            limit = int(request.args.get(cls._LIMIT_KEY, cls._LIMIT_DEFAULT))
            if limit < cls._LIMIT_MIN:
                raise ValueError(f'limit of "{limit}" is less than minimum "{cls._LIMIT_MIN}"')
            if limit > cls._LIMIT_MAX:
                raise ValueError(f'limit of "{limit}" is greater than maximum "{cls._LIMIT_MAX}"')
        except (TypeError, ValueError) as ex:
            abort(400)

        end = offset + limit

        tag_id = request.args.get(cls._TAG_KEY, None)
        try:
            tag_uuid = UUID(tag_id) if tag_id else None
        except (AttributeError, TypeError, ValueError) as ex:
            abort(400)

        with db_session:
            try:
                tag = TagEntity[tag_uuid] if tag_uuid else None
            except ObjectNotFound as ex:
                abort(400)

            selector = cls._selector(tag)

            sort = request.args.get(cls._SORT_KEY, cls._SORT_DEFAULT)

            try:
                order_by = cls._order_by(sort)
            except ValueError as ex:
                abort(400)

            user = current_user.get_entity()
            bookmarks = [bookmark for bookmark in user.bookmarks.select(selector).order_by(order_by)[offset:end]]
            output = cls._schema.dumps(bookmarks, many=True)

            return output

    @classmethod
    def post(cls):
        """Creates a new bookmark."""

        try:
            data = cls._schema.load(request.json)
        except ValidationError as ex:
            abort(400)

        with db_session:
            user = current_user.get_entity()
            bookmark = BookmarkEntity(label=data['label'], url=data['url'], text=data['text'],
                                      created=datetime.utcnow(), modified=datetime.utcnow(), user=user)

            output = cls._schema.dumps(bookmark)
            return output


class Tag(RestResource):
    """Represents an individual tag REST resource."""

    _schema = TagSchema()

    @classmethod
    def _get_tag(cls, tag_id):
        """Gets a REST appropriate output formatted tag from an ID."""

        try:
            uuid = UUID(tag_id)
        except ValueError as ex:
            abort(400)

        try:
            tag = TagEntity[uuid]
        except ObjectNotFound as ex:
            abort(404)

        output = cls._schema.dumps(tag)
        return output

    @classmethod
    def delete(cls, tag_id):
        """Deletes a tag.

        :param tag_id: ID of the tag to delete.
        :return: An HTTP response:
                 - If successful: 200 and a JSON representation of the deleted tag.
                 - If the tag is invalid (i.e., cannot be made into a UUID): 400
                 - If the tag doesn't exist: 404
        """

        try:
            uuid = UUID(tag_id)
        except ValueError as ex:
            abort(400)

        with db_session:
            try:
                tag = TagEntity[uuid]
            except ObjectNotFound as ex:
                abort(404)

            output = cls._schema.dumps(tag)

            tag.delete()

            return output

    @classmethod
    def get(cls, tag_id):
        """Gets a tag."""

        with db_session:
            output = cls._get_tag(tag_id)
            return output

    @classmethod
    def put(cls, tag_id):
        """Updates a tag."""

        abort(501)


class TagList(RestResource):
    """Represents a list of tags REST resource."""

    _schema = TagSchema()

    @classmethod
    def get(cls):
        """Gets the list of tags."""

        with db_session:
            user = current_user.get_entity()
            tags = list(user.tags)
            output = cls._schema.dumps(tags, many=True)
            return output

    @classmethod
    def post(cls):
        """Creates a new tag."""

        try:
            data = cls._schema.load(request.json)
        except ValidationError as ex:
            abort(400)

        with db_session:
            user = current_user.get_entity()
            tag = TagEntity(label=data['label'], user=user)

            output = cls._schema.dumps(tag)
            return output
