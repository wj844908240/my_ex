from flask import Blueprint


api = Blueprint('api', __name__,)


from api import UserApi
from api import UserAuthorityApi
from api import OpESApi