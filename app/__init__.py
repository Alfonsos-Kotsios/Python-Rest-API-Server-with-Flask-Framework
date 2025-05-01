from flask import Flask

server = Flask(__name__)

@server.route('/test')
def hello():
    return 'Hello, World! sThis is a test route.'


from app import routes

