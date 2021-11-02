#obj to connect to db and execute sql command
from pool_project import app
import os
import sqlite3

class ConnectionObject():
    database_uri = app.config['SERVER_LOCACTION']
    print(database_uri)
    def __init__(self):
        self.conn = sqlite3.connect(ConnectionObject.database_uri)
        self.c = self.conn.cursor()

    def get_inventory(self, filter_status=None):
        if filter_status:
            x = self.c.execute('select * from vw_inv_img_join').fetchall() 
        else:
            x = self.c.execute('select * from vw_inv_img_join').fetchall() 
        self.conn.close()
        return x
   
def convert_to_json(struct):
    ret_obj = {}
    for i in struct:
        ret_obj[i[-1]] = {'name': i[0], 'price': i[2], 'img': i[3]}
    #return str(ret_obj)
    return ret_obj

    
        
