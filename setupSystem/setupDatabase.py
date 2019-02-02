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


def config() :
    try:
        conn = db.connect(host = app.config['host'],user = app.config['user'],passwd = app.config['passwd'],db = app.config['db'] , charset='utf8',use_unicode=True)
        cursor = conn.cursor()
        print "<<<Creating users Tables>>>"
        # cursor.execute("create procedure dummy()")
        cursor.execute("DROP TABLE IF EXISTS users")
        conn.commit()
        cursor.execute("DROP TABLE IF EXISTS ClinicList")
        conn.commit()
        cursor.execute("DROP TABLE IF EXISTS Services")
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
        # create admin user
        import hashlib
        hash = hashlib.sha512('admin')
        hash = hash.hexdigest()
        query = """INSERT INTO users (name,username,password,RoleID) VALUES ('User Controler','admin','{0}','1')""".format(hash)
        cursor.execute(query)
        conn.commit()
        # clinics table
        query = """
            CREATE TABLE `ClinicList` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `clinic_id` INT(45) DEFAULT NULL,
            `ar_name` varchar(45) DEFAULT NULL,
            `en_name` varchar(45) DEFAULT NULL,
            `IsActive` varchar(45) DEFAULT NULL,
            `CreatedDate` datetime DEFAULT CURRENT_TIMESTAMP,
            `username` varchar (45) DEFAULT NULL,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """
        cursor.execute(query)
        conn.commit()
        # create Services table
        query = """
            CREATE TABLE `Services` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `serviceCode` int(29) DEFAULT NULL,
            `serviceAr` varchar(200) DEFAULT NULL,
            `serviceEN` varchar(200) DEFAULT NULL,
            `UserID` varchar(200) DEFAULT NULL,
            `IsActive` varchar(200) DEFAULT NULL,
            `clinic` varchar(200) DEFAULT NULL,
            `serviceCosting` varchar(200) DEFAULT NULL,
            `time` datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
        cursor.execute(query)
        conn.commit()

        # create payment methods table
        query = """
            CREATE TABLE `payment_methods` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `serviceCode` int(29) DEFAULT NULL,
            `serviceAr` varchar(200) DEFAULT NULL,
            `serviceEN` varchar(200) DEFAULT NULL,
            `UserID` varchar(200) DEFAULT NULL,
            `IsActive` varchar(200) DEFAULT NULL,
            `clinic` varchar(200) DEFAULT NULL,
            `serviceCosting` varchar(200) DEFAULT NULL,
            `time` datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
        cursor.execute(query)
        conn.commit()

        # print has.sha1('admin')
        print "All is Done enjoy ^_^"
    except NameError as e:
        # print NameError
        print "<<<Tables already exists>>>"


if __name__ == '__main__':
    config()
