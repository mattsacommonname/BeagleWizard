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


from flask import Flask
from flask_login import (
    LoginManager,
    UserMixin)
from pony.orm import (
    db_session,
    set_sql_debug)
from typing import Optional
from uuid import UUID

from config import config
from entities import (
    db,
    User as UserEntity)


# application

app = Flask(__name__)


# database

db.bind(**config.get('database_bindings', {'provider': 'sqlite', 'filename': ':memory:'}))
set_sql_debug(config.get('debug_mode', False))
db.generate_mapping(create_tables=config.get('create_tables', True))


# authentication

app.config['SECRET_KEY'] = config.get('secret_key')
login_manager = LoginManager(app)


class LoginUser(UserMixin):
    def __init__(self, user_entity: UserEntity):
        self.id = user_entity.id
        self.name = user_entity.name

    def get_entity(self) -> UserEntity:
        user_entity = UserEntity[self.id]
        return user_entity


@login_manager.user_loader
def load_user(user_id: str) -> Optional[UserMixin]:
    """User loader."""
    uuid = UUID(user_id)
    with db_session:
        user_entity = UserEntity[uuid]

        if not user_entity:
            return None

        user = LoginUser(user_entity)
        return user


# routes

import routes
