from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Print the entire GET request
        print(f"GET Request Path: {self.path}")
        print(f"GET Request Headers:\n{self.headers}")

        # Response body
        response = "Hello, this is the server response!"
        # Write content as utf-8 data
        self.wfile.write(bytes(response, "utf8"))
        return


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
