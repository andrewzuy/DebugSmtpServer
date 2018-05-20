from flask import Flask
import smtpd
import asyncore
import threading

emailStorage = []

class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, decode_data=True, **kwargs):
        print(data)
        emailStorage.append(str(data).replace('=3D','=').replace('=\n','\n').replace('&amp;','&'))
        emailStorage.append("\n=============================================================")

app = Flask(__name__)
app.debug = False

@app.route("/")
def hello():
    result = "============================================================="
    for data in emailStorage:
        result += "\n" + data
    return result

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