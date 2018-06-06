# -*- coding: utf-8 -*-
from config import db, app
#import settings
# app.config.from_object('config')
# app.config.from_object('settings')

from api import api


app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
