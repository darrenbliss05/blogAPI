import web
import json

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

if __name__ == "__main__":
#    Need to replace the hard-coded IP address with something that gets the IP adress of the current host
    web.httpserver.runsimple(app.wsgifunc(), ("192.168.1.18",8080))
    app.run()
