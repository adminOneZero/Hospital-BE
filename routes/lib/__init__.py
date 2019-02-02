from db import Connection
cursor , conn = Connection() # open Connection to db
class pagination(object):
    """docstring for pagination."""
    def __init__(self, inOnePage,tableName):
        self.inOnePage = inOnePage
        self.tableName = tableName

    def rowsInTable(self):
        q = """select count(*) from {0}""".format(self.tableName)
        result = cursor.execute(q)
        numOfRows = cursor.fetchall()
        rowsInTable = numOfRows[0][0] # all rows in services table
        return rowsInTable

    def paginate(self):
        from math import ceil
        btn_bar = int(ceil(self.rowsInTable() / float(self.inOnePage)))
        paginate = range(1,btn_bar+1) # numbers of bottoms for paginate system
        return paginate

    def offset(self,offset):
        offset = (offset - 1) * int(self.inOnePage)
        return offset
