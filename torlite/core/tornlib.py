# -*- coding:utf-8 -*-

import  tornado

class MultiStaticFileHandler(tornado.web.StaticFileHandler):
    def initialize(self, paths):
        self.paths = paths

    def get(self, path):
        for p in self.paths:
            try:
                # Initialize the Static file with a path
                super(MultiStaticFileHandler, self).initialize(p)
                # Try to get the file
                return super(MultiStaticFileHandler, self).get(path)
            except tornado.web.HTTPError as exc:
                # File not found, carry on
                if exc.status_code == 404:
                    continue
                raise
        # Oops file not found anywhere!
        raise tornado.web.HTTPError(404)