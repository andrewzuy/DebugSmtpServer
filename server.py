
from flask import Flask
import smtpd
import asyncore
import threading
import re

emailStorage = []

class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, decode_data=True, **kwargs):
        print(data)
        filter = re.compile("(?>From:).*")
        message = data.decode("utf-8").replace('=3D','=').replace('=\n','\n').replace('&amp;','&')
        if filter.match(message)!=None:
            emailStorage.append(filter.match(message))
        else:
            emailStorage.append(message)


app = Flask(__name__)
app.debug = False

@app.route("/")
def hello():
    result = "<html><h1>Debugging Email server</h1>"
    for data in emailStorage:
        result += "<hr><br>" + data
    return result + "</html>"

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
