# coding: utf-8
import unittest
import coverage

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User


COV = coverage.coverage(
        branch=True,
        include='project/*',
        omit=[
            'project/tests/*',
            'project/config.py',
            ],
    )
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    """
    Khởi tạo lại cơ sở dữ liệu
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Chạy các trường hợp kiểm thử"""
    tests = unittest.TestLoader().discover(
            'project/tests',
            pattern='test*.py',
            )
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def seed_db():
    """
    Tạo dữ liệu mẫu trong csdl
    """
    db.session.add(User(username='michael', email='michael@email.com'))
    db.session.add(User(username='somebody', email='somebody@email.com'))
    db.session.commit()


@cli.command()
def cov():
    """
    Chạy kiểm thử với coverage
    """
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()
