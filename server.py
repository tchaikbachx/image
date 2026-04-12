import os
import sys
import datetime
import sqlite3


# i rewrote some functions from /app in /mirror to run with
# server.py, so it does not trigger automatically; instead
# it communicates with the connection to get/set data,
# rather than interact with the database itself.

# here, it can be imported without executing the argv calls
# that were interrupting some script execution. there is a
# work-around, it will just not be finished by mvp-day.

# i am not a python pro, so there is probably a better way
# to handle it, this is just my quick fix for testing/dev
# purposes.


from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

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


# display all instruments in the database; i re-wrote this so that it performs
# lookups using checkout and instrument tables; that way, it will update when
# the server receives any changes that prompt a reload
@app.route('/api/instruments', methods=['GET'])
def get_instruments():
    conn = get_db_connection() 
    cur = conn.cursor()

    query = """
        SELECT i.*, 
        CASE 
            WHEN c.Item_ID IS NOT NULL THEN 'OUT' 
            ELSE 'IN' 
        END as Status
        FROM instrument i 
        LEFT JOIN checkout c ON i.Name_ID = c.Item_ID 
        AND c.Closed_Date = 'N/A'
    """
    
    cur.execute(query)
    instruments = [dict(row) for row in cur.fetchall()]
    
    conn.close()
    return jsonify(instruments)


# add an instrument to the database
@app.route('/api/instruments', methods=['POST'])
def add_instrument_endpoint():
    data = request.get_json()
    # try to load all the instruments if there are any
    try:
        conn = get_db_connection()
        new_id = group_add_logic(data, conn)
        # CODE 201: successfully added a new entry
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        # CODE 500: uh oh something went wrong here
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
            # CODE 200: success
            return jsonify({"status": "success"}), 200
        else:
            # CODE 404: did not find in database or accessing wrong db
            return jsonify({"status": "error", "message": "Instrument not found"}), 404
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500
    

# update the information about an instrument in the database
@app.route('/api/instruments/<int:instrument_id>', methods=['PUT'])
def update_instrument_endpoint(instrument_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        success = group_update_logic(instrument_id, data, conn)
        conn.close()
        # CODE 200: success
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500


# handling for checkins and checkouts
@app.route('/api/transaction', methods=['POST'])
def handle_transaction():
    data = request.json
    user_role = data.get('role') 
    
    # CODE 403: someone tried to bypass and larp as staff
    if user_role != 'staff':
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    item_id = data.get('item_id')
    action_type = data.get('type')
    today = datetime.date.today().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        if action_type == 'checkout':
            # get the next id
            cur.execute("SELECT MAX(ID) FROM checkout")
            res = cur.fetchone()[0]
            next_id = (res + 1) if res is not None else 1
            
            # map this to ID, Borrower_ID, Item_ID, Checkout_Date, Due_Date, Closed_Date
            cur.execute(
                "INSERT INTO checkout (ID, Borrower_ID, Item_ID, Checkout_Date, Due_Date, Closed_Date) VALUES (?, ?, ?, ?, ?, ?)",
                (next_id, data['borrower_email'], item_id, today, data['due_date'], "N/A")
            )

        elif action_type == 'checkin':
            # update Closed_Date to today to "close" the checkout
            cur.execute(
                "UPDATE checkout SET Closed_Date = ? WHERE Item_ID = ? AND Closed_Date = 'N/A'",
                (today, item_id)
            )

        conn.commit()
        # CODE 200: success
        return jsonify({"status": "success"}), 200
    except Exception as e:
        conn.rollback()
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()


# +----------------------------------------------------------------------------+
# |                                                                    SERVER  |
# +----------------------------------------------------------------------------+


# start the server!
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"opened at http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port)
