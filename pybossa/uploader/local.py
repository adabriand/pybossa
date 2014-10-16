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
# Cache global variables for timeouts
"""
Local module for uploading files to a PyBossa local filesystem.

This module exports:
    * Local class: for uploading files to a local filesystem.

"""
from pybossa.uploader import Uploader
import os
from werkzeug import secure_filename


class LocalUploader(Uploader):

    """Local filesystem uploader class."""

    upload_folder = 'uploads'
    pybossa_path = ''

    def init_app(self, app):
        """Config upload folder."""
        super(self.__class__, self).init_app(app)
        if app.config.get('UPLOAD_FOLDER'):
            self.upload_folder = app.config['UPLOAD_FOLDER']

    def _upload_file(self, file, container):
        """Upload a file into a container/folder."""
        try:
            filename = secure_filename(file.filename)
            if not os.path.isdir("/home/pybossa023/pybossa/pybossa/"+self.upload_folder+os.sep+container):
		os.makedirs("/home/pybossa023/pybossa/pybossa/"+self.upload_folder+os.sep+container)
	    file.save("/home/pybossa023/pybossa/pybossa/"+self.upload_folder+os.sep+container+os.sep+filename)
            return True
        except os.error as e:
            return False

    def delete_file(self, name, container):
        """Delete file from filesystem."""
        try:
            path = os.path.join(self.pybossa_path, self.upload_folder, container, name)
            os.remove(path)
            return True
        except:
            return False
