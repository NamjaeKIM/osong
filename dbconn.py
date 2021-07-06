#pip install psycopg2
import psycopg2

class dbConn() :
    def __init__(self) :
        self.conn = psycopg2.connect(host='localhost', dbname='postgres',user='postgres',password='admin',port=2345)
        #self.cursor = self.connect.cursor()

    # def __del__(self):
    #     self.connect.close()
    #     #self.cursor.close()

    # def opencursor(self) :
    #     self.cursor = self.db.cursor()

    # def closecursor(self) :
    #     self.cursor.close()

    def close(self):
        #self.cursor.commit()
        self.conn.close()

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        self.conn.close()
