import sys
from http.server import HTTPServer, BaseHTTPRequestHandler;
import MolDisplay
import molsql
import io

public_files = ['/style.css', '/script.js', '/index.html', '/add-molecules.html', '/view-molecules.html', '/add-elements.html', '/view-elements.html', '/logo.png']

# Subclass of BaseHTTPRequestHandler, used to run python webserver
class MyHandler(BaseHTTPRequestHandler):

    db = molsql.Database(True)
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
        if self.path == "/add-molecules.html":

            molecule = MolDisplay.Molecule()
            
            for i in range(0,4):    # skip 4 lines
                string = next(self.rfile)
            
            molecule.parse(string)
            molecule.sort()

            self.db.add_molecule()

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
