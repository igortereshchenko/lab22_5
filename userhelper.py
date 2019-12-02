from source.db import PostgresDb
from source.modelorm import ormTeacher


class UserHelper:

    def __init__(self):
        self.db = PostgresDb()

    @property
    def test(self):
        query = 'select * from public.teacher;'
        results = self.db.executes(query)
        print(results)
        return results


if __name__ == '__main__':
    db = PostgresDb()
    #teacher = UserHelper()
    #teacher.test()

    result = db.sqlalchemy_session.query(ormTeacher).all()
    for row in result:
        print(row.tc_info)
