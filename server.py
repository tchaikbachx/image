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


##################
# ADDING ENTRIES #
##################

# add a borrower to the database
@app.route('/api/borrower', methods=['POST'])
def add_borrower_endpoint():
    data = request.get_json()
    try:
        conn = get_db_connection()
        new_id = aBorr(conn, data.get('Email'))
        # CODE 201: successfully added a new entry
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# add a broken instrument to the database
@app.route('/api/broken', methods=['POST'])
def add_broken_endpoint():
    data = request.get_json()
    try:
        conn = get_db_connection()
        new_id = aBrok(conn, data.get('Item_ID'), data.get('Description'))
        # CODE 201: successfully added a new entry
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# add a checkout to the database
@app.route('/api/checkout', methods=['POST'])
def add_checkout_endpoint():
    data = request.get_json()
    try:
        conn = get_db_connection()
        new_id = aChec(conn, data.get('Borrower_ID'), data.get('Item_ID'), data.get('Due_Date'))
        # CODE 201: successfully added a new entry
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# add a department to the database
@app.route('/api/department', methods=['POST'])
def add_department_endpoint():
    data = request.get_json()
    try:
        conn = get_db_connection()
        new_id = aDepa(conn, data.get('Department_Name'))
        # CODE 201: successfully added a new entry
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# add an instrument to the database
@app.route('/api/instrument', methods=['POST'])
def add_instrument_endpoint():
    data = request.get_json()
    try:
        conn = get_db_connection()
        new_id = aInst(conn, data.get('Name_ID'), data.get('Old_ID'), data.get('Type'), data.get('Grade'), data.get('Make'), data.get('Model'), data.get('Picture'), data.get('Serial_Number'), data.get('Price'), data.get('Stored_In'), data.get('Dept'))
        # CODE 201: successfully added a new entry
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# add a (k)key to the database
@app.route('/api/kkey', methods=['POST'])
def add_kkey_endpoint():
    data = request.get_json()
    try:
        conn = get_db_connection()
        new_id = aKkey(conn, data.get('Name_ID'), data.get('Qty'), data.get('Description'))
        # CODE 201: successfully added a new entry
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# add a locker to the database
@app.route('/api/locker', methods=['POST'])
def add_locker_endpoint():
    data = request.get_json()
    try:
        conn = get_db_connection()
        new_id = aLock(conn, data.get('Name_ID'), data.get('Combo'), data.get('Kkey'), data.get('Checkoutable'))
        # CODE 201: successfully added a new entry
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# add a missing instrument to the database
@app.route('/api/missing', methods=['POST'])
def add_missing_endpoint():
    data = request.get_json()
    try:
        conn = get_db_connection()
        new_id = aMiss(conn, data.get('Item_ID'), data.get('Description'))
        # CODE 201: successfully added a new entry
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500
    

####################
# UPDATING ENTRIES #
####################

# update the information about a borrower in the database
@app.route('/api/borrower/<int:entry_id>', methods=['PUT'])
def update_borrower_endpoint(entry_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        success = uBorr(conn, entry_id, data.get('Email'))
        conn.close()
        # CODE 200: success
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# update the information about a broken instrument in the database
@app.route('/api/broken/<int:entry_id>', methods=['PUT'])
def update_broken_endpoint(entry_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        success = uBrok(conn, entry_id, data.get('Date_Broken'), data.get('Date_Fixed'), data.get('Item_ID'), data.get('Description'))
        conn.close()
        # CODE 200: success
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# update the information about a checkout in the database
@app.route('/api/checkout/<int:entry_id>', methods=['PUT'])
def update_checkout_endpoint(entry_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        success = uChec(conn, entry_id, data.get('Borrower_ID'), data.get('Item_ID'), data.get('Checkout_Date'), data.get('Due_Date'), data.get('Closed_Date'))
        conn.close()
        # CODE 200: success
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# update the information about a department in the database
@app.route('/api/department/<int:entry_id>', methods=['PUT'])
def update_department_endpoint(entry_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        success = uDepa(conn, entry_id, data.get('Department_Name'))
        conn.close()
        # CODE 200: success
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# update the information about an instrument in the database
@app.route('/api/instrument/<int:entry_id>', methods=['PUT'])
def update_instrument_endpoint(entry_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        success = uInst(conn, entry_id, data.get('Name_ID'), data.get('Old_ID'), data.get('Type'), data.get('Grade'), data.get('Make'), data.get('Model'), data.get('Picture'), data.get('Serial_Number'), data.get('Price'), data.get('Stored_In'), data.get('Dept'))
        conn.close()
        # CODE 200: success
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# update the information about a (k)key in the database
@app.route('/api/kkey/<int:entry_id>', methods=['PUT'])
def update_kkey_endpoint(entry_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        success = uKkey(conn, entry_id, data.get('Name_ID'), data.get('Qty'), data.get('Description'))
        # CODE 200: success
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500

# update the information about a locker in the database
@app.route('/api/locker/<int:entry_id>', methods=['PUT'])
def update_locker_endpoint(entry_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        success = uLock(conn, entry_id, data.get('Name_ID'), data.get('Combo'), data.get('Kkey'), data.get('Checkoutable'))
        # CODE 200: success
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500


# update the information about a missing instrument in the database
@app.route('/api/missing/<int:entry_id>', methods=['PUT'])
def update_missing_endpoint(entry_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        success = uMiss(conn, entry_id, data.get('Date_Missing'), data.get('Date_Found'), data.get('Item_ID'), data.get('Description'))
        # CODE 200: success
        return jsonify({"status": "success" if success else "no change"}), 200
    except Exception as e:
        # CODE 500: uh oh something went wrong here
        return jsonify({"status": "error", "message": str(e)}), 500


####################
# DELETING ENTRIES #
####################

# remove an instrument from the database
@app.route('/api/<str:table>/<int:entry_id>', methods=['DELETE'])
def delete_endpoint(table, entry_id):
    # try to load all the instruments if there are any
    try:
        conn = get_db_connection()
        success = deleteEntry(conn, table, entry_id)
        conn.close()
        
        if success:
            # CODE 200: success
            return jsonify({"status": "success"}), 200
        else:
            # CODE 404: did not find in database or accessing wrong db
            return jsonify({"status": "error", "message": "Item not found"}), 404
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
    print("opened at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
