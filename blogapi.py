
import json
import sqlite3
from flask import request, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
import socket
import os
import time
from daemonize import Daemonize
import logging
from sqlalchemy import create_engine, MetaData, Table


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/bliss/web/proj/blogAPI/blog.db'
db = SQLAlchemy(app)

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
        

#db = web.database(dbn="sqlite", db="blog.db")

# sqlite db schema from DBA does not include autoincrementing
# post_id. This is a workaround to get ths next available post_id
# during startup.
#
dbinstance = blogdb('blog.db')
post_id_counter = dbinstance.get_post_id_counter() - 1
dbinstance.closedb()  

class posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(8192), unique=False)
    title = db.Column(db.String(256), unique=False)

    def __init__(self, title, body,post_id):
        self.title = title
        self.body = body
        self.post_id = post_id
        print self.title, self.body, self.post_id

@app.route("/post",methods=['POST'])
def POST():
    global post_id_counter
    if not request.headers['Content-Type'] == 'application/json':
       return "MISSING JSON data"
    inputdata = json.loads(json.dumps(request.json))
    print inputdata['title']
    print inputdata['body']
    post_id_counter += 1
    postblog = posts(inputdata['title'], inputdata['body'], post_id_counter)
    db.session.add(postblog)
    db.session.commit()
    return "blog posted"

@app.route("/posts")
def GET():
    return "Requesting all blogs"

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

#if __name__ == "__main__":
def main():
    try:
        app.run(host=get_ip_address(), port=8080)
    except Exception, e:
        emsg = '%s' %(e)
        print emsg
        sys.exit(-1)


if __name__ == '__main__':
        if (len(sys.argv) > 1):
           if (sys.argv[1] == "--debug"):
               main()
               sys.exit()
       
        myname=os.path.basename(sys.argv[0])
        pidfile='/tmp/%s.pid' % myname       # any name
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        fh = logging.FileHandler("/tmp/blogsrcv.log", "w")
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        keep_fds = [fh.stream.fileno()]
        daemon = Daemonize(app=myname,pid=pidfile, action=main,keep_fds=keep_fds )
        daemon.start()
