from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import translate

# This class is used to handle http requests
class S(BaseHTTPRequestHandler):
    # This method is used to send response header to client
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    # This method is triggered when GET request is sent to server
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n",
                     str(self.path), str(self.headers))
        self._set_response()
        pageData = str.encode("404 NOT FOUND")
        if str(self.path) == "/" or str(self.path) == "/index.html":
            f = open("WebData/firstPage.htm", "rb")
            pageHtml = (f.read()).decode()
            pageBytes = formatMainPage(pageHtml)
            f.close()
            self.wfile.write(pageBytes)

    # This method is triggered when POST request is sent to server
    def do_POST(self):
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))
        pageData = str.encode("INCORRECT POST DATA")
        if len(post_data) >= 22 and str(self.path) == "/translate":
            pageData = formatResultPage(post_data)
        self._set_response()
        self.wfile.write(pageData)

# This function is used to format and display main webpage
def formatMainPage(html):
    return (html.replace("<REPLACE_WITH_LANGUAGES>", translate.getSupportedLanguagesForSelect())).encode()

# This function is used to format and display result webpage
def formatResultPage(post_data):
    splitData = post_data.decode().split('\r\n')
    language = splitData[0].split('=')[1]
    text = splitData[1].split('=')[1]
    text = text.replace("\r", "")
    translated_google, translated_deepl = translate.translate(language, text)
    if language[:3] == 'gt:': language = language[3:]
    f = open("WebData/translatePage.htm", "rb")
    pageHtml = (f.read()).decode()
    pageHtml = pageHtml.replace("{ORIGINAL_TEXT}", text)
    pageHtml = pageHtml.replace(
        "{TRANSLATED_TEXT_GOOGLE}", translated_google)
    pageHtml = pageHtml.replace(
        "{TRANSLATED_TEXT_DEEPL}", translated_deepl)
    pageHtml = pageHtml.replace("{SPECIFY_LANGUAGE}", language)
    pageData = pageHtml.encode('utf-8')
    f.close()
    return pageData

# This function is used to run HTTPServer with specified options
def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting ar http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

# Program starts here
if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
