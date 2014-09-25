# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2014 SF Isle of Man Limited
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.

import json
from flask import Response
from pybossa.model.user import User
from pybossa.core import db, get_locale
from pybossa.error import ErrorStatus

error = ErrorStatus()

class UserFbAPI():

    def get_user_by_fb_id(self, fb_user_id):
        return db.session.query(User).filter_by(facebook_user_id=fb_user_id).first()
    
    def create_fb_user(self, user_full_name, user_name, user_email, fb_user_id):
        try:
            account = User(fullname=user_full_name, name=user_name, email_addr=user_email)
            account.set_password(user_email)
            account.locale = get_locale()
            account.facebook_user_id = fb_user_id
            db.session.add(account)
            db.session.commit()
            return Response(json.dumps({"response": "OK"}),  mimetype="application/json")
        except Exception as e:
            return error.format_exception(e, target=self.__class__.__name__.lower(), action='CREATE_FB_USER')
    
    def update_fb_user(self, account, fb_user_id):
        try:
            account.facebook_user_id = fb_user_id
            db.session.add(account)
            db.session.commit()
            return Response(json.dumps({"response": "OK"}),  mimetype="application/json")
        except Exception as e:
            return error.format_exception(e, target=self.__class__.__name__.lower(), action='UPDATE_FB_USER')
