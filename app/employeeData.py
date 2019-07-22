"""This Employee Data Module is to serve REST APIs"""

from config import client
from app import app
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import request, jsonify, send_from_directory
import json
import ast
import imp
import logging


# Import the Utile module
utile_module = imp.load_source('*', './app/utile.py')

#setting logging
logging.basicConfig(level=logging.DEBUG)
logging.debug('This will get logged')

# Select the database
db = client.frederick
# Select the collection
collection = db.employees

# load the indexpage
# @app.route("/")
# def indexload ():
# 	 #disply index page
# 	return render_template('../template/index.html')

@app.route('/')
def indexload():
    return send_from_directory("templates/",'index.html')

@app.route("/api")
def get_api_initial_response():
    """API Welcome message"""

    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask REST API'
    }
     #Json response
    resp = jsonify(message)
    # Returning the response
    return resp


@app.route("/api/v1/employees", methods=['POST'])
def create_user():
    """
       Function to create new employee.
       """
    try:
        # Create new employee
        try:
            logging.debug('Inside employees post method')
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        record_created = collection.insert(body)

        # Prepare the response
        if isinstance(record_created, list):
            # Return list of Id of the newly created item
            return jsonify([str(v) for v in record_created]), 201
        else:
            # Return Id of the newly created item
            return jsonify(str(record_created)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/employees", methods=['GET'])
def fetch_users():
    """
       Function to fetch the users.
       """
    try:

        # Call the function to get the query params
        logging.debug('Inside employees get method')
        query_params = utile_module.parse_url_query_params(request.query_string)
        # Check if dictionary is not empty
        if query_params:
#            logging.error('%s raised an error', query_params)
            # Try to convert the value to int
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}

            # Fetch all the record(s)
            records_fetched = collection.find(query)

            # Check if the records are found
            if records_fetched.count() > 0:
                # Prepare the response
                return dumps(records_fetched)
            else:
                # No records are found
                return "", 404

        # If dictionary is empty
        else:
            # Return all the records as query string parameters are not available
            if collection.find().count > 0:
                # Prepare response if the users are found
                return dumps(collection.find())
            else:
                # Return empty array if no users are found
                return jsonify([])
    except:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/employees/<emp_id>", methods=['POST'])
def update_user(emp_id):
    """
       Function to update the user.
       """
    try:
        # Get the value which needs to be updated
        try:
            logging.debug('Inside employees post method with params')
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return "", 400

        # Updating the user
        records_updated = collection.update_one({"id": int(emp_id)}, body)

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            return "", 200
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return "", 404
    except:
        # Error while trying to update the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/employees/<id>", methods=['DELETE'])
def remove_user(id):
    """
       Function to remove the user.
       """
    try:
        # Delete the user
        logging.debug('Inside employees delete method')
        delete_user = collection.delete_one({'_id': ObjectId(id)})
        # logging.debug('%s number of deleted records',delete_user.deleted_count)
        if delete_user.deleted_count > 0 :
            # Prepare the response
            resp = jsonify('User deleted successfully!')
            return resp, 204
        else:
            # Resource Not found
            return "", 404
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp
