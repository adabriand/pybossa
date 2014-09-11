# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2013 SF Isle of Man Limited
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

from default import Test, assert_not_raises
from pybossa.auth import require
from nose.tools import assert_raises
from werkzeug.exceptions import Forbidden, Unauthorized
from mock import patch
from test_authorization import mock_current_user
from factories import AppFactory, BlogpostFactory, UserFactory
from factories import reset_all_pk_sequences



class TestBlogpostAuthorization(Test):

    mock_anonymous = mock_current_user()
    mock_authenticated = mock_current_user(anonymous=False, admin=False, id=2)
    mock_admin = mock_current_user(anonymous=False, admin=True, id=1)



    @patch('pybossa.auth.current_user', new=mock_anonymous)
    @patch('pybossa.auth.blogpost.current_user', new=mock_anonymous)
    def test_anonymous_user_create_given_blogpost(self):
        """Test anonymous users cannot create a given blogpost"""

        app = AppFactory.create()
        blogpost = BlogpostFactory.build(app=app, owner=None)

        assert_raises(Unauthorized, getattr(require, 'blogpost').create, blogpost)


    @patch('pybossa.auth.current_user', new=mock_anonymous)
    @patch('pybossa.auth.blogpost.current_user', new=mock_anonymous)
    def test_anonymous_user_create_blogposts_for_given_app(self):
        """Test anonymous users cannot create blogposts for a given project"""

        app = AppFactory.create()

        assert_raises(Unauthorized, getattr(require, 'blogpost').create, app_id=app.id)


    @patch('pybossa.auth.current_user', new=mock_anonymous)
    @patch('pybossa.auth.blogpost.current_user', new=mock_anonymous)
    def test_anonymous_user_create_blogposts(self):
        """Test anonymous users cannot create any blogposts"""


        assert_raises(Unauthorized, getattr(require, 'blogpost').create)


    @patch('pybossa.auth.current_user', new=mock_admin)
    @patch('pybossa.auth.blogpost.current_user', new=mock_admin)
    def test_non_owner_authenticated_user_create_given_blogpost(self):
        """Test authenticated user cannot create a given blogpost if is not the
        project owner, even if is admin"""

        admin = UserFactory.create()
        app = AppFactory.create()
        blogpost = BlogpostFactory.build(app=app, owner=admin)

        assert self.mock_admin.id != app.owner.id
        assert_raises(Forbidden, getattr(require, 'blogpost').create, blogpost)


    @patch('pybossa.auth.current_user', new=mock_admin)
    @patch('pybossa.auth.blogpost.current_user', new=mock_admin)
    def test_non_owner_authenticated_user_create_blogpost_for_given_app(self):
        """Test authenticated user cannot create blogposts for a given project
        if is not the project owner, even if is admin"""

        owner = UserFactory.create_batch(2)[1]
        app = AppFactory.create(owner=owner)

        assert self.mock_admin.id != app.owner.id
        assert_raises(Forbidden, getattr(require, 'blogpost').create, app_id=app.id)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_owner_create_given_blogpost(self):
        """Test authenticated user can create a given blogpost if is project owner"""

        owner = UserFactory.create_batch(2)[1]
        app = AppFactory.create(owner=owner)
        blogpost = BlogpostFactory.build(app=app, owner=owner)

        assert self.mock_authenticated.id == app.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').create, blogpost)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_owner_create_blogpost_for_given_app(self):
        """Test authenticated user can create blogposts for a given project
        if is project owner"""

        owner = UserFactory.create_batch(2)[1]
        app = AppFactory.create(owner=owner)

        assert self.mock_authenticated.id == app.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').create, app_id=app.id)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_owner_create_blogpost_as_other_user(self):
        """Test authenticated user cannot create blogpost if is project owner but
        sets another person as the author of the blogpost"""

        another_user = UserFactory.create()
        app = AppFactory.create()
        blogpost = BlogpostFactory.build(app_id=app.id,
                                          owner=another_user)

        assert self.mock_authenticated.id == app.owner.id
        assert_raises(Forbidden, getattr(require, 'blogpost').create, blogpost)


    @patch('pybossa.auth.current_user', new=mock_anonymous)
    @patch('pybossa.auth.blogpost.current_user', new=mock_anonymous)
    def test_anonymous_user_read_given_blogpost(self):
        """Test anonymous users can read a given blogpost"""

        app = AppFactory.create()
        blogpost = BlogpostFactory.create(app=app)

        assert_not_raises(Exception, getattr(require, 'blogpost').read, blogpost)


    @patch('pybossa.auth.current_user', new=mock_anonymous)
    @patch('pybossa.auth.blogpost.current_user', new=mock_anonymous)
    def test_anonymous_user_read_blogposts_for_given_app(self):
        """Test anonymous users can read blogposts of a given project"""

        app = AppFactory.create()
        assert_not_raises(Exception, getattr(require, 'blogpost').read, app_id=app.id)


    @patch('pybossa.auth.current_user', new=mock_anonymous)
    @patch('pybossa.auth.blogpost.current_user', new=mock_anonymous)
    def test_anonymous_user_read_given_blogpost_hidden_app(self):
        """Test anonymous users cannot read a given blogpost of a hidden project"""

        app = AppFactory.create(hidden=1)
        blogpost = BlogpostFactory.create(app=app)

        assert_raises(Unauthorized, getattr(require, 'blogpost').read, blogpost)


    @patch('pybossa.auth.current_user', new=mock_anonymous)
    @patch('pybossa.auth.blogpost.current_user', new=mock_anonymous)
    def test_anonymous_user_read_blogposts_for_given_hidden_app(self):
        """Test anonymous users cannot read blogposts of a given project if is hidden"""

        app = AppFactory.create(hidden=1)

        assert_raises(Unauthorized, getattr(require, 'blogpost').read, app_id=app.id)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_non_owner_authenticated_user_read_given_blogpost(self):
        """Test authenticated user can read a given blogpost if is not the project owner"""

        app = AppFactory.create()
        user = UserFactory.create()
        blogpost = BlogpostFactory.create(app=app)

        assert self.mock_authenticated.id != app.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').read, blogpost)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_non_owner_authenticated_user_read_blogposts_for_given_app(self):
        """Test authenticated user can read blogposts of a given project if
        is not the project owner"""

        app = AppFactory.create()
        user = UserFactory.create()

        assert self.mock_authenticated.id != app.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').read, app_id=app.id)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_non_owner_authenticated_user_read_given_blogpost_hidden_app(self):
        """Test authenticated user cannot read a given blogpost of a hidden project
        if is not the project owner"""

        app = AppFactory.create(hidden=1)
        user = UserFactory.create()
        blogpost = BlogpostFactory.create(app=app)

        assert self.mock_authenticated.id != app.owner.id
        assert_raises(Forbidden, getattr(require, 'blogpost').read, blogpost)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_non_owner_authenticated_user_read_blogposts_for_given_hidden_app(self):
        """Test authenticated user cannot read blogposts of a given project if is
        hidden and is not the project owner"""

        app = AppFactory.create(hidden=1)
        user = UserFactory.create()

        assert self.mock_authenticated.id != app.owner.id
        assert_raises(Forbidden, getattr(require, 'blogpost').read, app_id=app.id)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_owner_read_given_blogpost(self):
        """Test authenticated user can read a given blogpost if is the project owner"""

        owner = UserFactory.create_batch(2)[1]
        app = AppFactory.create(owner=owner)
        blogpost = BlogpostFactory.create(app=app)

        assert self.mock_authenticated.id == app.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').read, blogpost)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_owner_read_blogposts_for_given_app(self):
        """Test authenticated user can read blogposts of a given project if is the
        project owner"""

        owner = UserFactory.create_batch(2)[1]
        app = AppFactory.create(owner=owner)

        assert self.mock_authenticated.id == app.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').read, app_id=app.id)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_owner_read_given_blogpost_hidden_app(self):
        """Test authenticated user can read a given blogpost of a hidden project if
        is the project owner"""

        owner = UserFactory.create_batch(2)[1]
        app = AppFactory.create(owner=owner, hidden=1)
        blogpost = BlogpostFactory.create(app=app)

        assert self.mock_authenticated.id == app.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').read, blogpost)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_owner_read_blogposts_for_given_hidden_app(self):
        """Test authenticated user can read blogposts of a given hidden project if
        is the project owner"""

        owner = UserFactory.create_batch(2)[1]
        app = AppFactory.create(owner=owner, hidden=1)

        assert self.mock_authenticated.id == app.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').read, app_id=app.id)


    @patch('pybossa.auth.current_user', new=mock_admin)
    @patch('pybossa.auth.blogpost.current_user', new=mock_admin)
    def test_admin_read_given_blogpost_hidden_app(self):
        """Test admin can read a given blogpost of a hidden project"""

        admin = UserFactory.create()
        app = AppFactory.create(hidden=1)
        blogpost = BlogpostFactory.create(app=app)

        assert self.mock_admin.id != app.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').read, blogpost)


    @patch('pybossa.auth.current_user', new=mock_admin)
    @patch('pybossa.auth.blogpost.current_user', new=mock_admin)
    def test_admin_read_blogposts_for_given_hidden_app(self):
        """Test admin can read blogposts of a given hidden project"""

        admin = UserFactory.create()
        app = AppFactory.create(hidden=1)

        assert self.mock_admin.id != app.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').read, app_id=app.id)


    @patch('pybossa.auth.current_user', new=mock_anonymous)
    @patch('pybossa.auth.blogpost.current_user', new=mock_anonymous)
    def test_anonymous_user_update_blogpost(self):
        """Test anonymous users cannot update blogposts"""

        blogpost = BlogpostFactory.create()

        assert_raises(Unauthorized, getattr(require, 'blogpost').update, blogpost)


    @patch('pybossa.auth.current_user', new=mock_admin)
    @patch('pybossa.auth.blogpost.current_user', new=mock_admin)
    def test_non_owner_authenticated_user_update_blogpost(self):
        """Test authenticated user cannot update a blogpost if is not the post
        owner, even if is admin"""

        admin = UserFactory.create()
        app = AppFactory.create()
        blogpost = BlogpostFactory.create(app=app)

        assert self.mock_admin.id != blogpost.owner.id
        assert_raises(Forbidden, getattr(require, 'blogpost').update, blogpost)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_owner_update_blogpost(self):
        """Test authenticated user can update blogpost if is the post owner"""

        owner = UserFactory.create_batch(2)[1]
        app = AppFactory.create()
        blogpost = BlogpostFactory.create(app=app, owner=owner)

        assert self.mock_authenticated.id == blogpost.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').update, blogpost)


    @patch('pybossa.auth.current_user', new=mock_anonymous)
    @patch('pybossa.auth.blogpost.current_user', new=mock_anonymous)
    def test_anonymous_user_delete_blogpost(self):
        """Test anonymous users cannot delete blogposts"""

        blogpost = BlogpostFactory.create()

        assert_raises(Unauthorized, getattr(require, 'blogpost').delete, blogpost)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_non_owner_authenticated_user_delete_blogpost(self):
        """Test authenticated user cannot delete a blogpost if is not the post
        owner and is not admin"""

        blogpost = BlogpostFactory.create()

        assert self.mock_authenticated.id != blogpost.owner.id
        assert not self.mock_authenticated.admin
        assert_raises(Forbidden, getattr(require, 'blogpost').delete, blogpost)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    @patch('pybossa.auth.blogpost.current_user', new=mock_authenticated)
    def test_owner_delete_blogpost(self):
        """Test authenticated user can delete a blogpost if is the post owner"""

        owner = UserFactory.create_batch(2)[1]
        app = AppFactory.create()
        blogpost = BlogpostFactory.create(app=app, owner=owner)

        assert self.mock_authenticated.id == blogpost.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').delete, blogpost)


    @patch('pybossa.auth.current_user', new=mock_admin)
    @patch('pybossa.auth.blogpost.current_user', new=mock_admin)
    def test_admin_authenticated_user_delete_blogpost(self):
        """Test authenticated user can delete any blogpost if is admin"""

        admin = UserFactory.create()
        blogpost = BlogpostFactory.create()

        assert self.mock_admin.id != blogpost.owner.id
        assert_not_raises(Exception, getattr(require, 'blogpost').delete, blogpost)
