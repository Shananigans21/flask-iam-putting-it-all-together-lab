#!/usr/bin/env python3
import pytest
from server.app import create_app
from server.models import db
from server.app import app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

if __name__ == '__main__':
    create_tables()

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))
