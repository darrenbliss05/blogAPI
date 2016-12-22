import web
import json
import sqlite3
import sys

urls = (
    '/posts', 'posts',
    '/post' , 'post'
)

app = web.application(urls,globals())

class posts:
    def GET(self):
       allposts = {'post_id':1,'title':'testing','body':'this is a test'}
       web.header('Content-Type', 'application/json')
       return json.dumps(allposts)

class post:
    def POST(self):
       i = web.data()
       return i + '\n'

class blogdb:
    def __init__(self,dbfile):
        self.dbfile = dbfile
        #self.dbconnect = sqlite3.connect(self.dbfile)
        #self.dbcursor = self.dbconnect.cursor()
        self._opendb()
        #self.retrieve_all_posts()
        self._set_db_id_counter()
      #  self.db_id_counter = 0

    def _set_db_id_counter(self):
        self.db_id_counter = 1
        self.dbcursor.execute('select COALESCE(MAX(post_id)+1,0) from posts') 
        foo =  self.dbcursor.fetchone()[0]
        print foo
        print '\n'
        self.db_id_counter = int(foo)
        print self.db_id_counter
      
    def showtables(self):
        self.dbcursor.execute('.tables;') 
        print self.dbcursor.fetchall()
        
    def _opendb(self):
        self.dbconnect = sqlite3.connect(self.dbfile)
        self.dbconnect.text_factory = str
        self.dbcursor = self.dbconnect.cursor()

    def _closedb(self):
        self.dbconnect.close()
        
    def retrieve_all_posts(self):
        self.dbcursor.execute('select post_id,title,body from posts') 
        print self.dbcursor.fetchall()

    def write_to_db(self):
        title = "testing"
        body = "This is a test"
        self.dbcursor.execute('INSERT INTO posts VALUES (?,?,?)', (self.db_id_counter,title,body))
        self.dbconnect.commit()
        self.db_id_counter+=1
        

if __name__ == "__main__":
    dbinstance = blogdb('blog.db')
    dbinstance.write_to_db()
    dbinstance.write_to_db()
    dbinstance.retrieve_all_posts()
    sys.exit()
#    Need to replace the hard-coded IP address with something that gets the IP adress of the current host
    web.httpserver.runsimple(app.wsgifunc(), ("192.168.1.18",8080))
    app.run()
