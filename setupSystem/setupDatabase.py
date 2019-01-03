import MySQLdb as db
from flask import Flask
app = Flask(__name__)

app.config['host'] = '127.0.0.10'
app.config['user'] = 'root'
app.config['passwd'] = ''
app.config['db'] = 'hospital'


def Connection():
    conn = db.connect(host = app.config['host'],user = app.config['user'],passwd = app.config['passwd'],db = app.config['db'] , charset='utf8',use_unicode=True)
    cursor = conn.cursor()

    return cursor , conn




# print dir(cursor)
#
# cursor.execute("""
# INSERT INTO users (name,username,password) VALUES ('User Controler','admin','admin');
# ) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
# """)
# print cursor._query()
# print cursor._check_executed()
# print "<<<Connecting...>>>"
# cursor , conn = Connection()
def config() :
    try:
        conn = db.connect(host = app.config['host'],user = app.config['user'],passwd = app.config['passwd'],db = app.config['db'] , charset='utf8',use_unicode=True)
        cursor = conn.cursor()
        print "<<<Creating users Tables>>>"
        # cursor.execute("create procedure dummy()")
        cursor.execute("drop table if exists users")
        conn.commit()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `users` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `name` varchar(45) NOT NULL,
          `email` varchar(45) DEFAULT NULL,
          `username` varchar(45) NOT NULL,
          `password` varchar(512) NOT NULL,
          `userID` int(11) DEFAULT NULL,
          `RoleID` int(11) DEFAULT NULL,
          `Entrykey` varchar(45) DEFAULT NULL,
          `Telephone` varchar(45) DEFAULT NULL,
          `IsActive` bit(1) DEFAULT NULL,
          `CreatedBy` int(11) DEFAULT NULL,
          `ValidFrom` date DEFAULT NULL,
          `LastLogin` date DEFAULT NULL,
          `LastLogout` date DEFAULT NULL,
          `CreatedDate` date DEFAULT NULL,
          `CreatedTime` time DEFAULT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
        """)
        conn.commit()
        import hashlib
        hash = hashlib.sha512()
        hash = hash.hexdigest()
        query = """INSERT INTO users (name,username,password,RoleID) VALUES ('User Controler','admin','{0}','1')""".format(hash)
        cursor.execute(query)
        conn.commit()
        # print has.sha1('admin')
        print "All is Done enjoy ^_^"
    except NameError as e:
        # print NameError
        print "<<<Tables already exists>>>"


if __name__ == '__main__':
    config()
