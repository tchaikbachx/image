import os
import sys
import sqlite3

# i rewrote some functions from /app in /mirror to run with
# server.py, so it does not trigger automatically; instead
# it communicates with the connection to get/set data,
# rather than interact with the database itself.

# now, it can be imported without executing the argv calls
# that were interrupting script execution. there is a work-
# around, it will just not be finished by wednesday at all.

# i am not a python pro, so there is probably a better way
# to handle it, this is just my quick fix for
# testing/construction purposes.


from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# import all the local dependencies
from mirror.add_instrument import add_instrument as group_add_logic
from mirror.delete_instrument import delete_instrument as group_delete_logic
from mirror.update_instrument import update_instrument as group_update_logic

app = Flask(__name__)
CORS(app)

# get the correct paths for database connection
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'mirror', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# +----------------------------------------------------------------------------+
# |                                                            STATIC ROUTING  |
# +----------------------------------------------------------------------------+

# get the path to the homepage
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

# get the path to the dashboard
@app.route('/dashboard')
def dash():
    return send_from_directory('templates', 'dash.html')

# get the path to any dependencies of index or dash (i.e., script & style)
@app.route('/templates/<path:folder>/<path:filename>')
def send_template_assets(folder, filename):
    target_dir = os.path.join('templates', folder)
    return send_from_directory(target_dir, filename)

# +----------------------------------------------------------------------------+
# |                                                           DYNAMIC ROUTING  |
# +----------------------------------------------------------------------------+

# display all instruments in the database
@app.route('/api/instruments', methods=['GET'])
def get_instruments():
    # try to load all the instruments if there are any
    try:
        conn = get_db_connection()
        instruments = conn.execute('SELECT * FROM instrument').fetchall()
        conn.close()
        # convert the rows into list of dictionaries for js
        return jsonify([dict(row) for row in instruments])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# add an instrument to the database
@app.route('/api/instruments', methods=['POST'])
def add_instrument_endpoint():
    data = request.get_json()
    # try to load all the instruments if there are any
    try:
        conn = get_db_connection()
        new_id = group_add_logic(data, conn)
        # just for safety
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
# remove an instrument from the database
@app.route('/api/instruments/<int:instrument_id>', methods=['DELETE'])
def delete_instrument_endpoint(instrument_id):
    # try to load all the instruments if there are any
    try:
        conn = get_db_connection()
        success = group_delete_logic(instrument_id, conn)
        conn.close()
        
        if success:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Instrument not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
# update the information about an instrument in the database
@app.route('/api/instruments/<int:instrument_id>', methods=['PUT'])
def update_instrument_endpoint(instrument_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        success = group_update_logic(instrument_id, data, conn)
        conn.close()
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# +----------------------------------------------------------------------------+
# |                                                                    SERVER  |
# +----------------------------------------------------------------------------+

# try and start the server
if __name__ == '__main__':
    print("opened at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
