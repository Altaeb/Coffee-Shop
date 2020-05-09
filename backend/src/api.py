import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
@app.route('/drinks')
def get_drinks_representation():
    drinks=Drink.query.all()
    drinks_short=[drink.short() for drink in drinks]
    return jsonify({'success': True, 'drinks': drinks_short}), 200



@app.route('/drinks-detail')
@requires_auth(permission='get:drinks-detail')
def get_drinks_detail(permission):
    drinks=Drink.query.all()
    drinks_long=[drink.long() for drink in drinks]
    return jsonify({'success':True, 'drinks': drinks_long}), 200


@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def add_new_drink(permission):
    title = request.json.get('title')
    recipe=request.json.get('recipe')
    recipe_string = str(recipe).replace("\'", "\"")
    new_drink=Drink(title=title,recipe=recipe_string)
    new_drink.insert()
    drink=[new_drink.long()]
    return jsonify({'success': True, 'drinks':drink}), 200


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def modify_drink(permission, drink_id):
    drink=Drink.query.filter(Drink.id==drink_id).one_or_none()
    if not drink:
        abort(404)
    title=request.json.get('title')
    if title:
        drink.title=title
    recipe=request.json.get('recipe')
    if recipe:
        recipe_string = str(recipe).replace("\'", "\"")
        drink.recipe=recipe_string
    drink.update()
    return jsonify({'success': True, 'drinks':[drink.long()]}), 200

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(permission, drink_id):
    drink_to_delete=Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink_to_delete:
        abort(404)
    drink_to_delete.delete()
    return jsonify({'success':True,'delete': drink_id}), 200


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    'error': 404,
                    'message': "resource not found"
                    }), 404


@app.errorhandler(AuthError)
def authorization_failed(error):
    return jsonify({
                    "success": False,
                    'error': error.status_code,
                    'message': error.error['description'] 
                    }), error.status_code


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'success': False,
                    'error': 500,
                    'message': 'internal server error'
                    }), 500 
