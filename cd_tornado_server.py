
# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado chat application. By default will listen on port 8080.
"""
import os
import tornado.ioloop
import tornado.web
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer
import sockjs.tornado
import json
import time

import flaskr

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","root","flaskr" )

# prepare a cursor object using cursor() method
cursor = db.cursor()


curvote = 0

class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    participants = set()

    def on_open(self, info):
        # Send that someone joined
        self.broadcast(self.participants, "Someone joined.")
        self.send("{\"curvote\":%d}" % curvote)

        # Add client to the clients list
        self.participants.add(self)

    def on_message(self, message):
        # Broadcast message
        print json.dumps(json.loads(message), indent=2)
        cursor.execute("INSERT INTO entries(Title,Text) VALUES('%s','%s')" % ('Vote', message))
        db.commit()
        self.broadcast(self.participants, json.dumps(json.loads(message)))


    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.participants.remove(self)
        self.broadcast(self.participants, "Someone left.")

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create chat router
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/chat')
    
    wsgi_app = WSGIContainer(flaskr.app)

    # 2. Create Tornado application
    application = tornado.web.Application(
            ChatRouter.urls + [(r'.*', FallbackHandler, dict(fallback=wsgi_app))]
    )

    # 3. Make Tornado app listen on port 8080
    application.listen(8080)

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
