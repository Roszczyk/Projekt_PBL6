from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from collections import defaultdict
from pubsub_db import add_to_database, download_from_database
import time

def prepare_command_for_database(payload):
    document = dict()
    payload = defaultdict(lambda: None, payload)
    time = payload['timestamp'][0].split(".")[0]
    document.update({"timestamp" : time,"device_id" : payload['device_id'][0]})
    if payload['lights'] != None:
        document.update({"lights" : payload['lights'][0]})
    if payload['heating'] != None:
        document.update({"heating" : payload['heating'][0]})
    return document

class PostHandlerDatabase(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, db_addr, db_base, db_collection):
        self.db_addr = db_addr
        self.db_base = db_base
        self.db_collection = db_collection
        super().__init__(request, client_address, server)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)
        parsed_data = parse_qs(post_data.decode('utf-8'))
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'POST request received')
        document = prepare_command_for_database(parsed_data)
        print(document)
        add_to_database(document, self.db_addr, self.db_base, self.db_collection)

class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)
        parsed_data = parse_qs(post_data.decode('utf-8'))
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'POST request received')
        
        print(parsed_data)

def start_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PostHandler)
    print('Server running on port', port)
    httpd.serve_forever()

def server_to_database_init(port, db_addr, db_base, db_collection):
    server_address = ('', port)
    httpd = HTTPServer(server_address, lambda request, client_address, server: PostHandlerDatabase(request, client_address, server, db_addr, db_base, db_collection))
    print('Server running on port', port)
    return httpd

def server_to_database_loop(httpd):
    httpd.serve_forever()

def server_to_database(port, db_addr, db_base, db_collection):   
    server_address = ('', port)
    httpd = HTTPServer(server_address, lambda request, client_address, server: PostHandlerDatabase(request, client_address, server, db_addr, db_base, db_collection))
    print('Server running on port', port)
    httpd.serve_forever()