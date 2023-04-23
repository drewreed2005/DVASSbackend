import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            username = body.get('username')
            if username is None or len(username) < 1:
                return {'message': f'Username is missing, or is less than a character'}, 400
            # validate uid
            streak = body.get('streak')
            if streak is None or streak < 1:
                return {'message': f'Streak is missing, or is less than 1'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(username=username, 
                      streak=streak)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {username}, either a format error or a duplicate'}, 400

        def get(self): # Read Method
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

        def put(self):
            body = request.get_json() # get the body of the request
            id = body.get('id')
            username = body.get('username')
            streak = body.get('streak') # get the UID (Know what to reference)
            user = User.query.get(id) # get the player (using the uid in this case)
            user.update(username=username, streak=streak)
            return f"{user.read()} Updated"

        def delete(self):
            body = request.get_json()
            id = body.get('id')
            player = User.query.get(id)
            player.delete()
            return f"{player.read()} Has been deleted"

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    