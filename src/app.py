"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
members = jackson_family.get_all_members()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    
    response_body = {
        "family": jackson_family.get_all_members()
    }


    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"member": 'There is not member with provided id.'}), 400

    return jsonify({"member": member}), 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    request_data = request.get_json()
    if(member_id is None):
        return jsonify({"Message": 'You must provide an member_id'}), 400
    if request_data['first_name'] is not None and request_data['age'] is not None and request_data['name'] is not None and request_data['lucky_numbers'] is not None:
        member = jackson_family.get_member(member_id)
        if member is not None:
            jackson_family.delete_member(member)
            return jsonify({"members": jackson_family.get_all_members()})
        if member is None:
            return jsonify({"member": 'There is not member with provided id.'}), 400

@app.route('/members/<int:member_id>', methods=['POST'])
def add_member(member_id):
    request_data = request.get_json()
    if(member_id is None):
        return jsonify({"Message": 'You must provide an member_id'}), 400
    if request_data['first_name'] is not None and request_data['age'] is not None and request_data['name'] is not None and request_data['lucky_numbers'] is not None:
        jackson_family.add_member({"first_name": request_data['first_name'], "age": request_data['age'], "lucky_numbers": request_data['lucky_numbers'], "id": jackson_family._generateId() })
        return jsonify({"members": jackson_family.get_all_members()}),200
    else
        return jsonify({"message": "Bad request"}),400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
