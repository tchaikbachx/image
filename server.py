from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import sys, os

# --- PATH CONFIGURATION ---
# this should always be functional independent of machine so don't change it
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, 'app')

# add root and app folder to path
for path in [BASE_DIR, APP_DIR]:
    if path not in sys.path:
        sys.path.append(path)

# get path to the database
db_path = os.path.join(BASE_DIR, 'app', 'database.db')

# can import manager now that path is correct (do not move)
from manager import manager


# --- APP SETUP ---
app = Flask(__name__)
app.secret_key = 'grinnell_secret_key' # this will have to be changed for security
CORS(app)

db = manager(db_path)


# --- STATIC ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dash.html')


# --- GENERAL API ROUTES ---

@app.route('/api/<table_name>', methods=['GET'])
def get_entry(table_name):
    try:
        if request.method == 'GET':
            # join logic for the main instrument dash
            if table_name == 'instrument':
                data = db.status(table_name)
            else:
                data = db.fetch_all(table_name)
            return jsonify(data), 200

    except Exception as e:
        app.logger.error(f"API ERROR on {table_name}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/<table_name>/<int:entry_id>', methods=['PUT'])
def put_entry(table_name, entry_id):
    try:
        if request.method == 'PUT':
            data = request.get_json()
            for key in ['Status', 'ID']:
                data.pop(key, None)
            success = db.update(table_name, entry_id, data)
            return jsonify({"status": "updated" if success else "no change"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/<table_name>', methods=['POST'])
def add_entry(table_name):
    try:
        payload = request.get_json()
        new_id = db.add(table_name, payload) 
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/checkouts/<int:item_id>', methods=['GET'])
def get_item_checkouts(item_id):
    # for emails in sidebar
    query = """
        SELECT c.ID, b.Email, c.Due_Date 
        FROM checkout c
        JOIN borrower b ON c.Borrower_ID = b.ID
        WHERE c.Item_ID = ? AND c.Closed_Date IS NULL
    """
    results = db.query_db(query, (item_id,))
    return jsonify(results)


@app.route('/api/<table_name>/<int:entry_id>', methods=['DELETE'])
def delete_entry(table_name, entry_id):
    try:
        success = db.delete(table_name, entry_id) 
        return jsonify({"status": "deleted" if success else "not found"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- EXECUTION ---
if __name__ == '__main__':
    # log path for sanity
    print(f"--- DB PATH: {db_path} ---")
    app.run(host='0.0.0.0', port=5005, debug=True)

application = app