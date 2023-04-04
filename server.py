import sys
from http.server import HTTPServer, BaseHTTPRequestHandler;
import MolDisplay
import molsql
import urllib
import io

public_files = ['/style.css', '/script.js', '/index.html', '/add-molecules.html', '/add-molecules.js', '/view-molecules.html', '/add-elements.html', '/add-elements.js', '/view-elements.html', '/logo.png']

# Subclass of BaseHTTPRequestHandler, used to run python webserver
class MyHandler(BaseHTTPRequestHandler):

    db = molsql.Database(False)
    db.create_tables()

    # Presents the web-form
    def do_GET(self):
        # Display of web-page
        if self.path in public_files:
            self.send_response(200) 

            if self.path.endswith(".html"):
                self.send_header("Content-type", "text/html")

                fp = open (self.path[1:])
                page = fp.read()
                fp.close()

                self.send_header("Content-length", len(page))
                self.end_headers()

                self.wfile.write(bytes(page, "utf-8"))

            if self.path.endswith(".js"):
                self.send_header("Content-type", "text/javascript")

                script = open (self.path[1:], "rb")
                script_data = script.read()
                script.close()

                self.send_header("Content-length", len(script_data))
                self.end_headers()

                self.wfile.write(bytes(script_data))

            elif self.path.endswith(".png"):
                self.send_header("Content-type", "image/png")

                image = open (self.path[1:], "rb")
                image_data = image.read()
                image.close()

                self.send_header("Content-length", len(image_data))
                self.end_headers()

                self.wfile.write(bytes(image_data))

        else:
            # 404 error
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))

    # Sends an svg file to the client
    def do_POST(self):
        if self.path == "/molecule-add-handler.html":
            header_read = self.rfile.read(int(self.headers['content-length']))
            header_bytes = io.BytesIO(header_read)

            print ('reached this point')

            postvars = urllib.parse.parse_qs(header_read.decode('utf-8'))
            
            self.db.add_molecule(postvars.get('name')[0], io.StringIO(postvars.get('file')[0]))

            print ('Add successful')

        elif self.path == "/element-add-handler.html":
            print('Made it')
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length)

            postvars = urllib.parse.parse_qs(body.decode('utf-8'))
            
            self.db['Elements'] = (int(postvars.get('number')[0]), postvars.get('code')[0], postvars.get('name')[0], postvars.get('color1')[0][1:], postvars.get('color2')[0][1:], postvars.get('color3')[0][1:], int(postvars.get('radius')[0]))

        if self.path == "/molecule":
            # Reads contents of the previous webform and converts that data into
            # a TextIOWrapper
            header_read = self.rfile.read(int(self.headers['content-length']))
            header_bytes = io.BytesIO(header_read)
            header_text = io.TextIOWrapper(header_bytes)

            # Passing in of TextIOWrapper, where the molecule file is parsed sorted
            # and written to an SVG format
            molecule = MolDisplay.Molecule()
            molecule.parse(header_text)
            molecule.sort()
            svg_string = molecule.svg()

            # Display of SVG
            self.send_response(200)
            self.send_header("Content-type", "image/svg+xml")
            self.send_header("Content-length", len(svg_string))
            self.end_headers()

            self.wfile.write(bytes(svg_string, "utf-8"))
        else:
            # 404 error
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))


httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)

# Try except statement is to get rid of the messy message that shows
# when the user uses Ctrl+C to shut down the webserver
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('')

httpd.server_close()
