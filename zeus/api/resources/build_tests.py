from flask import request
from sqlalchemy.orm import contains_eager

from zeus.constants import Result
from zeus.models import Job, Build, TestCase

from .base_build import BaseBuildResource
from ..schemas import TestCaseSchema

testcases_schema = TestCaseSchema(many=True, strict=True)


class BuildTestsResource(BaseBuildResource):
    def get(self, build: Build):
        """
        Return a list of test cases for a given build.
        """
        query = TestCase.query.options(contains_eager('job')).join(
            Job,
            TestCase.job_id == Job.id,
        ).filter(
            Job.build_id == build.id,
        )

        result = request.args.get('result')
        if result:
            try:
                query = query.filter(TestCase.result == getattr(Result, result))
            except AttributeError:
                raise NotImplementedError

        return self.respond_with_schema(testcases_schema, query)
