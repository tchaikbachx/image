import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
<<<<<<< HEAD
from manager import manager
=======

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# import all the local dependencies
from app.addBorrower import addBorrower as aBorr
from app.addBroken import addBroken as aBrok
from app.addCheckout import addCheckout as aChec
from app.addDepartment import addDepartment as aDepa
from app.addInstrument import addInstrument as aInst
from app.addKkey import addKkey as aKkey
from app.addLocker import addLocker as aLock
from app.addMissing import addMissing as aMiss

from app.updateBorrower import updateBorrower as uBorr
from app.updateBroken import updateBroken as uBrok
from app.updateCheckout import updateCheckout as uChec
from app.updateDepartment import updateDepartment as uDepa
from app.updateInstrument import updateInstrument as uInst
from app.updateKkey import updateKkey as uKkey
from app.updateLocker import updateLocker as uLock
from app.updateMissing import updateMissing as uMiss

from app.deleteEntry import deleteEntry
>>>>>>> refs/remotes/origin/main


app = Flask(__name__)
CORS(app)


<<<<<<< HEAD
db_path = os.path.join(os.path.dirname(__file__), 'mirror', 'database.db')
db = manager(db_path)
=======
# get the correct paths for database connection
def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'mirror', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
>>>>>>> refs/remotes/origin/main

@app.route('/')
def index():
    return send_from_directory(os.path.join(BASE_DIR, 'templates'), 'index.html')

@app.route('/dashboard')
<<<<<<< HEAD
def dashboard():
    return send_from_directory('templates', 'dash.html')
=======
def dash():
    return send_from_directory(os.path.join(BASE_DIR, 'templates'), 'dash.html')
>>>>>>> refs/remotes/origin/main

@app.route('/templates/<path:path>')
def send_assets(path):
    return send_from_directory('templates', path)


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
<<<<<<< HEAD
    print("Server opened successfully without error on port 5000")
    app.run(debug=True, port=5000)
=======
    port = int(os.environ.get("PORT", 5000))
    print(f"opened at http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port)

application = app
>>>>>>> refs/remotes/origin/main
