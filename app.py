import json

import tornado.ioloop
import tornado.web
import tornado.websocket

usernames = set()
listeners = set()
id_counter = 0


class AppHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('main.html')


class ChatSocketHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.username = ''

    def open(self):
        global id_counter

        listeners.add(self)

        id_counter += 1
        new_username = 'user' + str(id_counter)

        usernames.add(new_username)
        self.username = new_username

        message = {'username': new_username}
        self.write_message(json.dumps(message))

    def on_message(self, message):
        message_dict = {
            'from': self.username,
            'message': message
        }

        for listener in listeners:
            listener.write_message(json.dumps(message_dict))

    def on_close(self):
        usernames.discard(self.username)
        listeners.discard(self)


app = tornado.web.Application(
    handlers=[
        (r'/', AppHandler),
        (r'/chat', ChatSocketHandler)
    ],
    template_path='templates/',
    static_path='static/',
    autoreload=True
)

if __name__ == '__main__':
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()