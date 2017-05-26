from flask import request

from models import User, BucketList, Item
from run import db

@app.route('auth/register', methods=['POST'])
def register():
	pass

@app.route('auth/login', methods=['POST'])
def login():
	pass

@app.route('/bucketlists/', methods=['POST', 'GET'])
def add_bucketlist():
    pass

def view_bucket_lists():
	pass

@app.route('/bucketlists/<id>', methods=['GET', 'PUT', 'DELETE'])
def view_single_bucket_list():
 	pass

def edit_single_bucket_list():
	pass

def delete_single_bucket_list():
	pass

@app.route('/bucketlists/<id>/items/', methods=['GET'])
def add_item():
	pass

@app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT', 'DELETE'])
def edit_single_item():
	pass

def delete_single_item():
	pass