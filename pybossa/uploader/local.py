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
    #pybossa_path = ''

    def init_app(self, app):
        """Config upload folder."""
        super(self.__class__, self).init_app(app)
        if app.config.get('UPLOAD_FOLDER'):
            self.upload_folder = app.config['UPLOAD_FOLDER']

    def _upload_file(self, file, container):
        """Upload a file into a container/folder."""
	dat = open("/tmp/teste.log", "w")
        try:
	    dat.write("1")
            filename = secure_filename(file.filename)
	    dat.write("2")
            #if not os.path.isdir(os.path.join(self.pybossa_path, self.upload_folder, container)):
            if not os.path.isdir("/home/pybossa023/pybossa/pybossa/"+self.upload_folder+os.sep+container):
		#dat.write("tentando make"+str(os.path.join(self.pybossa_path, self.upload_folder, container))+" " + os.stat(os.path.join(self.pybossa_path)).st_mode)
                dat.write("UID" + str(os.geteuid())+" " +str(os.stat("/home/pybossa023/pybossa")) + " " + str(os.stat("/home/pybossa023/pybossa/pybossa")))
 		#os.makedirs(os.path.join(self.pybossa_path, self.upload_folder, container))
		os.makedirs("/home/pybossa023/pybossa/pybossa/"+self.upload_folder+os.sep+container)
		dat.write("2.1")
	    dat.write("Trying to save\n")
            #file.save(os.path.join(self.pybossa_path, self.upload_folder, container, filename))
	    file.save("/home/pybossa023/pybossa/pybossa/"+self.upload_folder+os.sep+container+os.sep+filename)
	    dat.write("saved")
	    dat.close()
            return True
        except os.error as e:
	    dat.write("Not saved"+str(e))
	    dat.close()
            return False

    def delete_file(self, name, container):
        """Delete file from filesystem."""
        try:
            path = os.path.join(self.pybossa_path, self.upload_folder, container, name)
            os.remove(path)
            return True
        except:
            return False
