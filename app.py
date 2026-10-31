from flask import Flask, jsonify, request

app = Flask(__name__)
items = {}

@app.get('/health')
def health():
    return jsonify(status='OK'), 200

@app.get('/count')
def count():
    return jsonify(count=len(items)), 200

@app.get('/songs')
def list_items():
    return jsonify(list(items.values())), 200

@app.get('/songs/<int:item_id>')
def get_item(item_id):
    if item_id not in items:
        return jsonify(error='Not found'), 404
    return jsonify(items[item_id]), 200

@app.post('/songs')
def create_item():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='JSON object required'), 400
    item_id = max(items, default=0) + 1
    items[item_id] = {'id': item_id, **data}
    return jsonify(items[item_id]), 201

@app.put('/songs/<int:item_id>')
def update_item(item_id):
    if item_id not in items:
        return jsonify(error='Not found'), 404
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='JSON object required'), 400
    items[item_id].update({k: v for k, v in data.items() if k != 'id'})
    return jsonify(items[item_id]), 200

@app.delete('/songs/<int:item_id>')
def delete_item(item_id):
    if item_id not in items:
        return jsonify(error='Not found'), 404
    del items[item_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
