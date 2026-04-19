import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from manager import manager


app = Flask(__name__)
CORS(app)

# Get the absolute path to the directory where server.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tell Flask explicitly where to find your files
app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'templates'))

@app.route('/')
def index():
    # Use BASE_DIR instead of 'db' to find the folder
    return send_from_directory(os.path.join(BASE_DIR, 'templates'), 'index.html')

@app.route('/dashboard')
def dash():
    return send_from_directory(os.path.join(BASE_DIR, 'templates'), 'dash.html')


db_path = os.path.join(os.path.dirname(__file__), 'mirror', 'database.db')
db = manager(db_path)

# @app.route('/')
# def index():
#     return send_from_directory(os.path.join(db, 'templates'), 'index.html')

# @app.route('/dashboard')
# def dash():
#     return send_from_directory(os.path.join(db, 'templates'), 'dash.html')

# @app.route('/templates/<path:path>')
# def send_assets(path):
#     return send_from_directory('templates', path)


# ignore this, will abstract static routes out later maybe

# @app.route('/', defaults={'page': 'index'})
# @app.route('/<page>')
# def pages(page):
#     filename = page if page.endswith('.html') else f"{page}.html"
#     return send_from_directory('templates', filename)

# def assets(folder, filename):
#     return send_from_directory(os.path.join('templates', folder), filename)


@app.route('/api/<table_name>', methods=['GET'])
def get_table(table_name):
    try:
        data = db.status() if table_name == 'instrument' else db.fetch(table_name)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 501
    

@app.route('/api/<table_name>', methods=['POST'])
def add_table(table_name):
    try:
        data = request.get_json()
        new_id  = db.add(table_name, data)
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 502


@app.route('/api/<table_name>/<int:entry_id>',methods=['PUT'])
def update_table(table_name, entry_id):
    try:
        data = request.get_json()
        success = db.update(table_name, entry_id, data)
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 503
    

@app.route('/api/<table_name>/<int:entry_id>', methods=['DELETE'])
def delete_entry(table_name, entry_id):
    try:
        success = db.delete(table_name, entry_id)
        return jsonify({"status": "success" if success else "not found"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 504


if __name__ == '__main__':
    print("Server opened successfully without error on port 5000")
    app.run(debug=True, port=5000)
