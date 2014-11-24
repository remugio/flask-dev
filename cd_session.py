import uuid, time

class Session:
    def __init__(self, sessionid, create_time, username, token):
        self.sessionid = sessionid
        self.create_time = create_time
        self.username = username
        self.token = token

def create(db, username):
    if username is None:
        return None
    query_str = 'INSERT INTO {0} ({1}, {2}, {3}) values ({4}, {5}, {6})'.format(TABLE_NAME, FIELD_CREATETIME, FIELD_USERNAME, FIELD_TOKEN, '%s', '%s', '%s')
    token = str(uuid.uuid4())
    create_time = int(time.time())
    db.cursor().execute(query_str, [create_time, username, token])
    db.commit()
    return token

def get_all_by_username(db, username):
    if username is None:
        return []
    query_str = 'SELECT {0}, {1}, {2}, {3} FROM {4} WHERE {5}={6}'.format( FIELD_SESSIONID, FIELD_CREATETIME, FIELD_USERNAME, FIELD_TOKEN, TABLE_NAME, FIELD_USERNAME, '%s')
    cur = db.cursor()
    cur.execute(query_str, [username])
    entries = [Session(row[0], row[1], row[2], row[3]) for row in cur.fetchall()]
    return entries

def delete_all_by_username(db, username):
    if username is None:
        return
    query_str = 'DELETE FROM {0} WHERE {1}={2}'.format(TABLE_NAME, FIELD_USERNAME, '%s')
    db.cursor().execute(query_str, [username])
    db.commit()

def is_valid_token(db, username, session_token):
    sessions = get_all_by_username(db, username)
    print(map(lambda x: x.token, sessions))
    return session_token in map(lambda x: x.token, sessions)

##################
# DB Definitions #
##################
TABLE_NAME = 'sessions'
FIELD_SESSIONID = 'id'
FIELD_CREATETIME = 'createtime'
FIELD_USERNAME = 'username'
FIELD_TOKEN = 'token'
