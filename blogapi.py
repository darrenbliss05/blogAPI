
import web
import json
import sqlite3
import sys
import socket
import os
from daemonize import Daemonize
import logging
#import daemon

urls = (
    '/posts', 'posts',
    '/post' , 'post'
)

app = web.application(urls,globals())

class blogdb:
    def __init__(self,dbfile):
        self.dbfile = dbfile
        self._opendb()
        self._set_db_id_counter()

    def _set_db_id_counter(self):
        self.db_id_counter = 1
        self.dbcursor.execute('select COALESCE(MAX(post_id)+1,0) from posts') 
        foo =  self.dbcursor.fetchone()[0]
        self.db_id_counter = int(foo)
      
    def get_post_id_counter(self):
        return(self.db_id_counter)

    def _opendb(self):
        self.dbconnect = sqlite3.connect(self.dbfile)
        self.dbconnect.text_factory = str
        self.dbcursor = self.dbconnect.cursor()

    def closedb(self):
        self.dbconnect.close()
        

db = web.database(dbn="sqlite", db="blog.db")

# sqlite db schema from DBA does not include autoincrementing
# post_id. This is a workaround to get ths next available post_id
# during startup.
#
dbinstance = blogdb('blog.db')
post_id_counter = dbinstance.get_post_id_counter()
dbinstance.closedb()  


class posts:
    def GET(self):
       web.header('Content-Type', 'application/json')
       t = db.transaction()
       results =  db.query("select * from posts")
       return (json.dumps( [dict(ix) for ix in results] ))

class post:
    def POST(self):
       global post_id_counter
       data = json.loads(web.data())
       t = db.transaction()
       my_post_id = post_id_counter
       post_id_counter += 1
       try:
          n = db.insert('posts', title=data["title"],body=data["body"],post_id=my_post_id)
       except Exception, e:
          emsg = 'ERROR: %s\n'  %(e)
          print  emsg 
       else:
          t.commit()
       return()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

#if __name__ == "__main__":
def main():
    try:
       #web.config.debug = False
       web.httpserver.runsimple(app.wsgifunc(), (get_ip_address(),8080))
    except Exception, e:
        emsg = '%s' %(e)
        print emsg
        sys.exit(-1)


if __name__ == '__main__':
       #main()
        myname=os.path.basename(sys.argv[0])
        pidfile='/tmp/%s' % myname       # any name
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        fh = logging.FileHandler("/tmp/test.log", "w")
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        keep_fds = [fh.stream.fileno()]
        daemon = Daemonize(app=myname,pid=pidfile, action=main,keep_fds=keep_fds )
        daemon.start()
