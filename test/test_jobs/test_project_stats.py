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

from pybossa.jobs import get_project_jobs, create_dict_jobs, get_project_stats
from default import Test, with_context
from factories import ProjectFactory
from factories import UserFactory


class TestProjectsStats(Test):


    @with_context
    def test_create_dict_job(self):
        """Test JOB create dict job works."""
        user = UserFactory.create(pro=True)
        project = ProjectFactory.create(owner=user)
        from sqlalchemy.sql import text
        from pybossa.core import db
        sql = text('''SELECT project.id, project.short_name FROM project, "user"
                   WHERE project.owner_id="user".id AND "user".pro=True;''')
        results = db.slave_session.execute(sql)
        jobs_generator = create_dict_jobs(results, get_project_stats, (10 * 60))
        jobs = []
        for job in jobs_generator:
            jobs.append(job)

        err_msg = "There should be only one job"
        assert len(jobs) == 1, err_msg

        job = jobs[0]
        assert 'get_project_stats' in job['name'].__name__
        assert job['args'] == [project.id, project.short_name]

    @with_context
    def test_get_project_jobs(self):
        """Test JOB get project jobs works."""
        user = UserFactory.create(pro=True)
        project = ProjectFactory.create(owner=user)
        jobs_generator = get_project_jobs()
        jobs = []
        for job in jobs_generator:
            jobs.append(job)
        err_msg = "There should be only one job"

        assert len(jobs) == 1, err_msg

        job = jobs[0]
        err_msg = "There should have the same name, but it's: %s" % job['name']
        assert "get_project_stats" == job['name'].__name__, err_msg
        err_msg = "There should have the same args, but it's: %s" % job['args']
        assert [project.id, project.short_name] == job['args'], err_msg
        err_msg = "There should have the same kwargs, but it's: %s" % job['kwargs']
        assert {} == job['kwargs'], err_msg

    @with_context
    def test_get_project_jobs_for_non_pro_users(self):
        """Test JOB get project jobs works for non pro users."""
        ProjectFactory.create()
        jobs_generator = get_project_jobs()
        jobs = []
        for job in jobs_generator:
            jobs.append(job)

        err_msg = "There should be only 0 jobs"
        assert len(jobs) == 0, err_msg
