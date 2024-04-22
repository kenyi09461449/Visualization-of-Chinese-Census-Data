from flask import Flask
from application.controller.api import api

'''app init'''
app = Flask(__name__, static_folder='static', static_url_path='')

'''app secret'''
app.secret_key = "popanalyz"

"""register api router"""
app.register_blueprint(api, url_prefix='')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)