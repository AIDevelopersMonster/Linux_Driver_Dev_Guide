from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial


class Handler(SimpleHTTPRequestHandler):
    extensions_map = SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map[".css"] = "text/css"
    extensions_map[".js"] = "text/javascript"
    extensions_map[".txt"] = "text/plain; charset=utf-8"


handler = partial(Handler, directory="docs/_build/html")
server = ThreadingHTTPServer(("127.0.0.1", 8001), handler)

print("Serving docs at http://127.0.0.1:8001/")
server.serve_forever()