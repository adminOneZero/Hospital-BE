import MySQLdb as db
config = {}
config['host'] = '127.0.0.10'
config['user'] = 'root'
config['passwd'] = ''
config['db'] = 'hospital'


def Connection():
    conn = db.connect(host = config['host'],user = config['user'],passwd = config['passwd'],db = config['db'] , charset='utf8',use_unicode=True)
    cursor = conn.cursor()

    return cursor , conn
