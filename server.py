
from flask import Flask
import smtpd
import asyncore
import threading
import re
import quopri


emailStorage = []

class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, decode_data=True, **kwargs):
        print(data)
        message = quopri.decodestring(data).decode("utf-8")#.replace('=3D','=').replace('=\n','').replace('&amp;','&').replace('=0D','\r').replace('=0A','\n')
        emailStorage.append(message)


app = Flask(__name__)
app.debug = False

@app.route("/")
def print_emails():
    result = "<html><h1>Debugging Email server</h1>"
    for data in emailStorage:
        result += "<hr><br>" + data
    return result + "</html>"

@app.route("/clear")
def clear_emails():
    del emailStorage[:]
    return "<html><h1>All emails were cleared</h1><br><h2><a href=\"http://uscourt.ga\">Back to emails</a></h2></html>"

def run_http():
    print("running")
    app.run(host='0.0.0.0',port=80)

def run_smtp():
    server = CustomSMTPServer(('0.0.0.0', 25), None)
    asyncore.loop()

if __name__ == '__main__':
    smtpTh = threading.Thread(target = run_smtp)
    smtpTh.start()
    run_http()
