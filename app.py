import tornado.ioloop
import tornado.web

class AppHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Hello, World!')

app = tornado.web.Application([
    (r'/', AppHandler),
])

if __name__ == '__main__':
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()