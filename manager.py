#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import current_app
from flask_script import Manager, prompt_bool
from werkzeug.contrib.fixers import ProxyFix
from gevent.wsgi import WSGIServer

from website import app, db, configured_app
from website.config import DevConfig, ProdConfig
from website.data import populate_data
from website.model import User


def create_app_manager(config):
    if config == "prod":
        return configured_app(app, ProdConfig())
    else:
        return configured_app(app, DevConfig())


manager = Manager(create_app_manager)


@manager.command
def initdb():
    "Creates database tables and insert data"
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        db.create_all()
        populate_data()


@manager.shell
def make_shell_context():
    return dict(app=current_app, db=db, User=User)


manager.add_option('-c', '--config',
                   dest="config",
                   default='dev',
                   choices=('prod', 'dev'))


@manager.command
def runserver():
    """Runs the Flask server"""
    if app.debug:
        app.run(host=app.config['HOST'], port=app.config['PORT'])
    else:
        app.wsgi_app = ProxyFix(app.wsgi_app)
        address = app.config['HOST'], app.config['PORT']
        server = WSGIServer(address, app)
        try:
            print("Server running on port %s:%d. Ctrl+C to quit" % address)
            server.serve_forever()
        except KeyboardInterrupt:
            server.stop()
    print("\nBye bye")


if __name__ == "__main__":
    manager.run()
