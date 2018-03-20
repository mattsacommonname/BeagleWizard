# Copyright 2018 Matthew Bishop
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

from config import config
from entities import db as database, User as UserEntity
from flask import Flask
from flask_login import LoginManager
from pony.orm import db_session, set_sql_debug
from uuid import UUID


# application

application = Flask(__name__)


# database

database.bind(**config.get('database_bindings', {'provider': 'sqlite', 'filename': ':memory:'}))
set_sql_debug(config.get('debug_mode', False))
database.generate_mapping(create_tables=config.get('create_tables', True))


# authentication

application.config['SECRET_KEY'] = config.get('secret_key')
login_manager = LoginManager(application)


@login_manager.user_loader
def load_user(user_id):
    """User loader."""
    uuid = UUID(user_id)
    with db_session:
        user = UserEntity[uuid]
        return user


# routes

import routes
