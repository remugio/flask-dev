class User:
    def __init__(self, userid, username, passhash):
        self.userid = userid
        self.username = username
        self.passhash = passhash

def create(db, username, passhash):
    query_str = 'INSERT INTO {0} ({1}, {2}) values ({3}, {4})'.format(TABLE_NAME, FIELD_USERNAME, FIELD_PASSHASH, '%s', '%s')
    db.cursor().execute(query_str, [username, passhash])
    db.commit()

def get_all_by_username(db, username):
    query_str = 'SELECT {0}, {1}, {2} FROM {3} WHERE {4}={5}'.format(FIELD_USERID, FIELD_USERNAME, FIELD_PASSHASH, TABLE_NAME, FIELD_USERNAME, '%s')
    cur = db.cursor()
    cur.execute(query_str, [username])
    entries = [User(row[0], row[1], row[2]) for row in cur.fetchall()]
    return entries

def get_one_by_username(db, username):
    entries = get_all_by_username(db, username)
    return None if len(entries) < 1 else entries[0]

def username_taken(db, username):
    entries = get_all_by_username(db, username)
    return len(entries) > 0

##################
# DB Definitions #
##################
TABLE_NAME = 'users'
FIELD_USERID = 'id'
FIELD_USERNAME = 'username'
FIELD_PASSHASH = 'passhash'
