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


from flask_login import login_required
from flask_restful import Resource


class Bookmark(Resource):
    decorators: [login_required]

    @staticmethod
    def get(bookmark_id):
        return {'id': bookmark_id}


class BookmarkList(Resource):
    decorators: [login_required]

    @staticmethod
    def get():
        return []


class Tag(Resource):
    decorators: [login_required]

    @staticmethod
    def get(tag_id):
        return {'id': tag_id}


class TagList(Resource):
    decorators: [login_required]

    @staticmethod
    def get():
        return []
