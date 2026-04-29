import sqlite3

# this function, when given a connection, will return a formatted string of all 
# the borrowers' emails. It will look like "email@email.com; email@email.com; ..."
# will be useful for mass emailing!
def getFULLemaillist(conn: Connection):
    # set cursor for db interaction
    cur = conn.cursor()

    # loop over checkout table
    # grab all the emails of still active rows
    cur.execute("SELECT Borrower_ID FROM checkout WHERE Closed_Date IS NULL")

    # get list of borrower ids (formatting is icky)
    rawList = cur.fetchall()
    # print(rawList)

    # format the ids
    Borrower_ID_List = []

    for item in rawList:
        Borrower_ID_List.append(item[0])

    # print(Borrower_ID_List)

    #remove duplicates!!
    Borrower_ID_List = set(Borrower_ID_List)

    # print(Borrower_ID_List)

    # extract the emails!
    Email_List = []

    for id in Borrower_ID_List:
        query = "SELECT Email FROM borrower WHERE ID = ?"
        cur.execute(query, (str(id)))
        # cur.execute("SELECT Email FROM borrower WHERE ID = ?", (str(id)))
        Email_List.append(cur.fetchone()[0])
    
    # format email list!
    email_string = "muschkot@grinnell.edu"

    for email in Email_List:
        email_string += "; " 
        email_string += email

    # print(email_string)

    return email_string