# imports --------------------------------------------------------------------+

import os
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS

from manager import manager

# --------------------------- DO NOT CHANGE THIS ----------------------------+

# get the abs path to the directory (kept same naming conventions as in .wsgi)
BASE_DIR = os.environ.get('PROJECT_ROOT', os.path.dirname(os.path.abspath(__file__)))


# set up the server variable and load it with the correct file paths.
# >> path should always be /templates/ for the raw html and anything else
#    is in /templates/<folder> (for scripts and styling)
app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)


# get the path of the database itself independent of the machine, then set it
# up with the manager to funnel commands through.
# >> database resides in its own container when deployed
db_path = os.path.join(os.path.dirname(__file__), 'app', 'database.db')
db = manager(db_path)

# ----------------------------- STATIC ROUTING -------------------------------+

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dash.html')

# # when viewing homepage, append the '/' tag to the url
# @app.route('/')
# def index():
#     return send_from_directory(app.template_folder, 'index.html')


# # when viewing dashboard, append the '/dashboard' tag to the url
# @app.route('/dashboard')
# def dash():
#     return send_from_directory(app.template_folder, 'dash.html')


# # this may be deprecated
# @app.route('/templates/<path:filename>')
# def stat(filename):
#     return send_from_directory(app.static_folder, filename)

# ------------------------------- TEMP LOGIN ---------------------------------+

app.secret_key = 'grinnell_secret_key' # necessary to gain permissions

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # hardcoded credentials
    if username == "admin" and password == "1234":
        session['is_staff'] = True # set flag
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route('/logout')
def logout():
    session.pop('is_staff', None)
    return redirect(url_for('index'))

# ----------------------------- DYNAMIC ROUTING ------------------------------+

# generalized get method, are used for any function that retrieves the data.
# >> EX: displaying instruments in cards and additional instrument information
@app.route('/api/<table_name>', methods=['GET'])
def get_table(table_name):
    try:
        data = db.status() if table_name == 'instrument' else db.fetch(table_name)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 501
    

@app.route('/api/instrument', methods=['POST'])
def add_instrument():
    try:
        data = request.get_json()
        # sanitize the data
        data.pop('Status', None)
        data.pop('ID', None) 
        
        new_id = db.add('instrument', data)
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        print(f"Add Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 502
    

@app.route('/api/checkout', methods=['POST'])
def checkout_api():
    data = request.get_json()
    email = data.get('email')
    item_id = data.get('Item_ID')
    due_date = data.get('Due_Date')

    # find or create borrower
    borrower = db.fetch('borrower')
    borrower_match = next((b for b in borrower if b['Email'] == email), None)
    
    if not borrower_match:
        borrower_id = db.add('borrower', {'Email': email})
    else:
        borrower_id = borrower_match['ID']

    # add checkout to record
    db.add('checkout', {
        'Borrower_ID': borrower_id,
        'Item_ID': item_id,
        'Due_Date': due_date
    })
    
    return jsonify({"status": "success"}), 201


@app.route('/api/history/<item_id>')
def get_history(item_id):
    # join two databases (checkout/instruments)
    query = """
        SELECT c.*, b.Email 
        FROM checkout c
        JOIN borrower b ON c.Borrower_ID = b.ID
        WHERE c.Item_ID = ?
        ORDER BY c.Checkout_Date DESC
    """
    with db.get() as conn:
        cur = conn.cursor()
        cur.execute(query, (item_id,))
        return jsonify([dict(row) for row in cur.fetchall()])


@app.route('/api/instrument/<int:entry_id>', methods=['PUT'])
def update_instrument(entry_id):
    try:
        data = request.get_json()
        
        data.pop('Status', None)
        data.pop('ID', None)
        
        success = db.update('instrument', entry_id, data)
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        print(f"Update Error on ID {entry_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 503


# generalized delete method; there is only one 'delete' method, but it
# can be used in multiple tables.
@app.route('/api/instrument/<int:entry_id>', methods=['DELETE'])
def delete_instrument(entry_id):
    try:
        success = db.delete('instrument', entry_id)
        return jsonify({"status": "success" if success else "not found"}), 200
    except Exception as e:
        print(f"Delete Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 504


# for debugging purposes when running on local ports; it should not be
# included in the live version
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"opened at http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port)

application = app
