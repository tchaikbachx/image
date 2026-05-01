from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import sys, os

# +------------------------------------------------------------+
# |                                  SET THE PATHS/STATES      |
# +------------------------------------------------------------+

# this should always be functional independent of machine now,
# so don't change it
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, 'app')

# add root and app folder to path
for path in [BASE_DIR, APP_DIR]:
    if path not in sys.path:
        sys.path.append(path)

# get path to the database
db_path = os.path.join(BASE_DIR, 'app', 'database.db')

# can import manager now that path is correct (do not move, has
# to be after path init)
from manager import manager

app = Flask(__name__)

# this will have to be changed for security later
app.secret_key = 'grinnell_secret_key'

CORS(app)

db = manager(db_path)


# +------------------------------------------------------------+
# |                                       STATIC ROUTING       |
# +------------------------------------------------------------+

# home path for URL
@app.route('/')
def index():
    return render_template('index.html')

# dashboard path for URL
@app.route('/dashboard')
def dashboard():
    return render_template('dash.html')
    

@app.route('/logout')
def logout():
    session.clear() # This wipes is_staff and user_id
    return redirect(url_for('index'))


# +------------------------------------------------------------+
# |                                        DYNAMIC ROUTING     |
# +------------------------------------------------------------+

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # using a hardcoded check, will need to change
    if username == "admin" and password == "1234":
        session['is_staff'] = True
        session['user_id'] = "staff_member"
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "unauthorized"}), 401


# route for students to browse items without edit/delete tools
@app.route('/inventory')
def student_inventory():
    # ensure is_staff is False or None
    session['is_staff'] = False 
    return render_template('dash.html')


# protected route for staff management
@app.route('/dashboard')
def staff_dashboard():
    if not session.get('is_staff'):
        return redirect(url_for('login'))
    return render_template('dash.html')


# [add defn]
@app.route('/api/<table_name>/<int:entry_id>', methods=['PUT'])
def put_entry(table_name, entry_id):
    try:
        data = request.get_json()
        # don't send metadata to update
        for key in ['Status', 'Availability', 'Loan_Count', 'ID', 'Key_Name', 'Locker_Name']:
            data.pop(key, None)

        if not data:
            return jsonify({"status": "no changes to update"}), 200
                    
        success = db.update(table_name, entry_id, data)
        if not success:
             return jsonify({"error": "Database update failed"}), 400
        return jsonify({"status": "updated"}), 200
    except Exception as e:
        # [DEBUG] log the error in console
        app.logger.error(f"Update Error: {e}")
        return jsonify({"error": str(e)}), 500
    

# [add defn]
@app.route('/api/checkout', methods=['POST'])
def checkout_item():
    data = request.json
    item_id = data.get('item_id')
    email = data.get('email')
    due_date = data.get('due_date')
    item_type = data.get('item_type') # 'instrument', 'locker', or 'kkey'

    # this is deprecated but i am still transferring some testing so i kept it
    item_name = db.get_name_by_type(item_type, item_id)

    for key in ['Status', 'Availability', 'Loan_Count', 'ID', 'Key_Name', 'Locker_Name']:
        data.pop(key, None)

    if not data:
            return jsonify({"status": "no changes to update"}), 200

    # specific error messages for qol debugging
    if not item_id:
        return jsonify({"error": "Server received no item_id"}), 400
    if not email:
        return jsonify({"error": "Server received no email"}), 400
    if not due_date:
        return jsonify({"error": "Server received no due_date"}), 400

    success = db.add_checkout(item_id, email, due_date, item_type)
    
    if success:
        return jsonify({"status": "success", "message": "Checkout recorded"}), 200
    else:
        return jsonify({"status": "failed", "message": "Database error or borrower not found"}), 500

    
# [add defn]
@app.route('/api/<table_name>', methods=['POST'])
def add_entry(table_name):
    try:
        payload = request.get_json()
        new_id = db.add(table_name, payload) 
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# [add defn]
@app.route('/api/<table_name>', methods=['GET'])
def get_entry(table_name):
    try:
        if request.method == 'GET':
            # check if the table is one of the primary dashboard items
            if table_name in ['instrument', 'kkey', 'locker']:
                data = db.status(table_name)
            else:
                # fetch borrowers, departments, etc
                data = db.fetch_all(table_name)
            return jsonify(data), 200

    except Exception as e:
        app.logger.error(f"API ERROR on {table_name}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/checkouts/<int:item_id>', methods=['GET'])
def get_item_checkouts(item_id):
    query = """
        SELECT c.ID, b.Email, c.Due_Date, c.Checkout_Date 
        FROM checkout c
        JOIN borrower b ON c.Borrower_ID = b.ID
        WHERE c.Item_ID = ? AND (c.Closed_Date IS NULL OR c.Closed_Date = '')
    """
    with db.get_conn() as conn:
        cur = conn.cursor()
        cur.execute(query, (item_id,))
        return jsonify([dict(row) for row in cur.fetchall()])


@app.route('/api/history/<string:name_id>', methods=['GET'])
def get_item_history(name_id):
    # block on the data
    if not session.get('is_staff'):
        return jsonify({"error": "Unauthorized"}), 403
        
    query = """
        SELECT c.ID, b.Email, c.Due_Date, c.Closed_Date
        FROM checkout c
        JOIN borrower b ON c.Borrower_ID = b.ID
        JOIN instrument i ON c.Item_ID = i.ID
        WHERE i.Name_ID = ?
        ORDER BY c.ID DESC
    """
    with db.get_conn() as conn:
        cur = conn.cursor()
        cur.execute(query, (name_id,))
        return jsonify([dict(row) for row in cur.fetchall()])


# handles checking an item back in
@app.route('/api/return/<int:loan_id>', methods=['POST'])
def return_item(loan_id):
    success = db.generalized_return(loan_id)
    return jsonify({"status": "success" if success else "failed"}), 200


# [add defn]
@app.route('/api/<table_name>/<int:entry_id>', methods=['DELETE'])
def delete_entry(table_name, entry_id):
    try:
        success = db.delete(table_name, entry_id) 
        return jsonify({"status": "deleted" if success else "not found"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# +------------------------------------------------------------+
# |                                       START THE SERVER     |
# +------------------------------------------------------------+

# start up the server (remove debugging for deployment)
if __name__ == '__main__':
    # [DEBUG] stdout the log path for sanity
    print(f"--- DB PATH: {db_path} ---")
    app.run(host='0.0.0.0', port=5005, debug=True)

application = app