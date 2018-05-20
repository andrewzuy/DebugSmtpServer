from flask import Flask
import smtpd
import asyncore
import threading
import email

emailStorage = []

class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, decode_data=True, **kwargs):
        print(data)
        msg = email.message_from_bytes(data)
        #emailStorage.append(str(data).replace('=3D','=').replace('=\n','\n').replace('&amp;','&'))
        if msg.is_multipart():
            for payload in msg.get_payload():
                # if payload.is_multipart(): ...
                emailStorage.append(payload.get_payload())
        else:
            emailStorage.append(msg.get_payload())


app = Flask(__name__)
app.debug = False

@app.route("/")
def hello():
    result = "<html><h1>Debugging email server</h1>"
    for data in emailStorage:
        result += "<hr>" + data
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