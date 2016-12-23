#!/bin/python
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
from flask_marshmallow import Marshmallow

app_internal_configurations = {"install_path": "/opt/blogsrv", "pidfile_path":"/opt/blogsrv", "logfile_path":"/opt/blogsrv","database_file":"blog.db"} 

def get_config():
    global app_internal_configurations 

    mydir=os.path.dirname(os.path.realpath(__file__))
    configfile = "%s/%s" %(mydir,"configfile")
    try:
       confile = open(configfile,"r")
       configs = json.loads(confile.read().strip())
       confile.close()
    except IOError:
       sys.write.stderr("Could not open config file %s" %(configfile)) 
       sys.exit(1)

    if 'logfile_path' in configs.keys():
        app_internal_configurations['logfile_path'] = configs['logfile_path']
    if 'install_path' in configs.keys():
        app_internal_configurations['install_path'] = configs['install_path']
    if 'pidfile_path' in configs.keys():
        app_internal_configurations['pidfile_path'] = configs['pidfile_path']
    if 'database_file' in configs.keys():
        app_internal_configurations['database_file'] = configs['database_file']
    return

get_config()

app = Flask(__name__)
ma = Marshmallow(app)

# This really should be reading from a SQLALCHEMY configuration file. 
dbfile = 'sqlite:///%s/%s' %(app_internal_configurations['install_path'], app_internal_configurations['database_file'])
app.config['SQLALCHEMY_DATABASE_URI'] = dbfile 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
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

class postschema(ma.Schema):
    class Meta:
      fields = ('post_id', 'body', 'title')

posts_schema = postschema(many=True)


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
    resultSet = posts.query.all()
    result = posts_schema.dump(resultSet)
    return json.dumps(result)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

from signal import SIGTERM
def shutdown(pidfile):
    print "Reading pidfile is %s" % pidfile  
    try:
       pidf = open(pidfile,"r")
       pid = int(pidf.readline().strip())
       pidf.close()
    except IOError:
       pid = None
    print "PID is %s\n" % pid
    if not pid:
      message = "pidfile %s does not exits. Daemon is not running\n"
      sys.stderr.write(message % pidfile)
      return

    try:
      while 1:
          os.kill(pid,SIGTERM)
          time.sleep(1)
    except OSError, err:
      err = str(err)
      if (err.find("No such process") > 0):
           if (os.path.exists(pidfile)):
                   os.remove(pidfile)
      else: 
           print str(err)
           sys.exit(1)

     

#if __name__ == "__main__":
def main():
    try:
        app.run(host=get_ip_address(), port=8080)
    except Exception, e:
        emsg = '%s' %(e)
        print emsg
        sys.exit(-1)


if __name__ == '__main__':
        myname=os.path.basename(sys.argv[0])
        pidpath = app_internal_configurations['pidfile_path']
        pidfile='%s/%s.pid' %(pidpath,myname)

        if (len(sys.argv) > 1):
           if (sys.argv[1] == "--debug"):
               main()
               sys.exit()
           elif (sys.argv[1] == "stop"):
               shutdown(pidfile) 
               sys.exit()

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        logfile = "%s/blogsrv.log" %app_internal_configurations['logfile_path']
        fh = logging.FileHandler(logfile, "w")
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        keep_fds = [fh.stream.fileno()]
        daemon = Daemonize(app=myname,pid=pidfile, action=main,keep_fds=keep_fds )
        daemon.start()

