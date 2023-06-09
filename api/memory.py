import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.memories import Memory

memory_api = Blueprint('memory_api', __name__,
                   url_prefix='/api/memory')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(memory_api)

# using insertion sort to sort the memory times
def insertion_sort(list, key):
    for i in range(1, len(list)):
        current = list[i]
        j = i - 1
        while j >= 0 and current[key] < list[j][key]:
            list[j + 1] = list[j]
            j -= 1
        list[j + 1] = current
    return list

class MemoryAPI:        
    class _Create(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            username = body.get('username')
            if username is None or len(username) < 1:
                return {'message': f'Username is missing, or is less than a character'}, 400
            # validate uid
            seconds = body.get('seconds')
            if seconds is None or seconds < 1:
                return {'message': f'Seconds is missing, or is less than 1'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Memory(username=username, 
                      seconds=seconds)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {username}, either a format error or a duplicate'}, 400

    class _Read(Resource):
        def get(self): # Read Method
            users = Memory.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            json_ready = insertion_sort(json_ready, "seconds")
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    class _Update(Resource):
        def put(self):
            body = request.get_json() # get the body of the request
            id = body.get('id')
            username = body.get('username')
            seconds = body.get('seconds') # get the UID (Know what to reference)
            user = Memory.query.get(id) # get the player (using the uid in this case)
            user.update(username=username, seconds=seconds)
            return f"{user.read()} Updated"

    class _Delete(Resource):
        def delete(self):
            body = request.get_json()
            id = body.get('id')
            player = Memory.query.get(id)
            player.delete()
            return f"{player.read()} Has been deleted"

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Update, '/update')
    api.add_resource(_Delete, '/delete')
    