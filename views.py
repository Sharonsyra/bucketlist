from random import randint

from flask import request, Flask, jsonify, abort, make_response, url_for

from models import User, BucketList, Item
from run import db

app = Flask(__name__)

bucketlists =[
{
    'id': 1,
    'name': "Bucketlist1",
    'items': [
        {
'id': 1,
'name': "I need to do X",
'date_created': "2015-08-12 11:57:23",
'date_modified': "2015-08-12 11:57:23",
'done': False
}
],
    'done': False,
    'date_created': "2015-08-12 11:57:23",
    'date_modified': "2015-08-12 11:57:23",
    'created_by': "1113456"
},
{
    'id': 2,
    'name': "Bucketlist2",
    'items': [
        {
'id': 1,
'name': "I need to do X",
'date_created': "2015-08-12 11:57:23",
'date_modified': "2015-08-12 11:57:23",
'done': False
}
],
    'done': False,
    'date_created': "2015-08-12 11:57:23",
    'date_modified': "2015-08-12 11:57:23",
    'created_by': "1113456"
}
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def make_public_task(item):
    new_item = {}
    for field in item:
        if field == 'id':
            new_item['uri'] = url_for('get_item', item_id=item['id'], _external=True)
        else:
            new_item[field] = item[field]
    return new_item

def make_public_task(bucketlist):
    new_bucketlist = {}
    for field in bucketlist:
        if field == 'id':
            new_bucketlist['uri'] = url_for('get_bucketlist', id=bucketlist['id'], _external=True)
        else:
            new_bucketlist[field] = bucketlist[field]
    return new_bucketlist

@app.route('/api/v1.0/auth/register', methods=['POST'])
def register():
    pass

@app.route('/api/v1.0/auth/login', methods=['POST'])
def login():
    pass

@app.route('/api/v1.0/bucketlists/', methods=['GET'])
def get_bucketlists():
    # return jsonify({'bucketlists': bucketlists})
    return jsonify({'bucketlists': [make_public_task(bucketlist) for bucketlist in bucketlists]})

@app.route('/api/v1.0/bucketlists/', methods=['POST'])
def add_bucketlist():
    if not request.json or not 'name' in request.json:
        abort(400)
    bucketlist = {
        # 'id': bucketlists[-1]['id'] + 1,
        'id': randint(1, 100),
        'name': request.json['name'],
        'items': request.json.get('items', []),
        'done': False,
}
    bucketlists.append(bucketlist)
    return jsonify({'bucketlist': bucketlist}), 201

@app.route('/api/v1.0/bucketlists/<int:id>', methods=['GET'])
def get_bucketlist(id):
    bucketlist = [bucket_list for bucket_list in bucketlists if bucket_list['id'] == id]
    if len(bucketlist) == 0:
        abort(404)
    return jsonify({'bucketlist': bucketlist[0]})

@app.route('/api/v1.0/bucketlists/<int:id>', methods=['PUT'])
def edit_single_bucket_list(id):
    bucketlist = [bucket_list for bucket_list in bucketlists if bucket_list['id'] == id]
    if len(bucketlist) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'items' in request.json and type(request.json['items']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    bucketlist[0]['name'] = request.json.get('name', bucketlist[0]['name'])
    bucketlist[0]['items'] = request.json.get('items', bucketlist[0]['items'])
    bucketlist[0]['done'] = request.json.get('done', bucketlist[0]['done'])
    return jsonify({'bucketlist': bucketlist[0]})

@app.route('/api/v1.0/bucketlists/<int:id>', methods=['DELETE'])
def delete_single_bucket_list(id):
    bucketlist = [bucket_list for bucket_list in bucketlists if bucket_list['id'] == id]
    if len(bucketlist) == 0:
        abort(404)
    bucketlists.remove(bucketlist[0])

    return jsonify({'msg': "Bucketlist deleted successfully."})

@app.route('/api/v1.0/bucketlists/<id>/items/', methods=['POST'])
def add_item(id):
    if not request.json or not 'name' in request.json:
        abort(400)
    item = {
        # 'id': bucketlists[-1]['id'] + 1,
        'id': randint(1, 100),
        'name': request.json['name'],
        'done': False,
}
    bucketlists[0]['items'].append(item)
    return jsonify({'item': item}), 201

@app.route('/api/v1.0/bucketlists/<id>/items/', methods=['GET'])
def get_items(id):
    # return jsonify({'items': bucketlists[0]['items']})
    return jsonify({'items': [make_public_task(item) for item in bucketlists[0]['items']]})

@app.route('/api/v1.0/bucketlists/<id>/items/<int:item_id>', methods=['GET'])
def get_item(id, item_id):
    item = [item_object for item_object in bucketlists[0]['items'] if item_object['id'] == item_id]
    if len(item) == 0:
        abort(404)
    return jsonify({'item': item[0]})

@app.route('/api/v1.0/bucketlists/<id>/items/<int:item_id>', methods=['PUT'])
def edit_single_item(id, item_id):
    item = [item_object for item_object in bucketlists[0]['items'] if item_object['id'] == item_id]
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    item[0]['name'] = request.json.get('name', item[0]['name'])
    item[0]['done'] = request.json.get('done', item[0]['done'])
    return jsonify({'item': item[0]})

@app.route('/api/v1.0/bucketlists/<id>/items/<int:item_id>', methods=['DELETE'])
def delete_single_item(id, item_id):
    item = [item_object for item_object in bucketlists[0]['items'] if item_object['id'] == item_id]
    if len(item) == 0:
        abort(404)
    bucketlists[0]['items'].remove(item[0])

    return jsonify({'msg': "Bucketlist deleted successfully."})

if __name__ == '__main__':
    app.run(debug=True)
