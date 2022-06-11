from gevent import monkey
monkey.patch_all()

from app.app import app

app
