import threading
import time

from flask import Flask, send_file, render_template, request, url_for
import signal
import hashlib
import os
import sys

app = Flask(__name__)
print(sys.argv)
main_password = sys.argv[1]
file_path = bytes.fromhex(sys.argv[2]).decode("utf-8")
"""main_password = ""
file_path = """""
print(main_password, file_path)

@app.route("/")
def home():
    return render_template("index.html")

def shutdown_server():
    time.sleep(1)
    print("Shutting down gracefully...")

    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'

@app.route('/shutitdown', methods=['GET'])
def shutdown():
    t1 = threading.Thread(target=shutdown_server)
    t1.start()
    return 'Server shutting down...'

@app.route("/download", methods=["Get"])
def download_file():
    password = request.args.get("p")

    f = send_file(file_path, as_attachment=True)
    if password != None:
        if hashlib.sha256(main_password.encode("utf-8")).hexdigest() == hashlib.sha256(password.encode("utf-8")).hexdigest():
            return f
        else:
            return "<h1>Nope! File is forbidden!!! Enter the correct password</h1> <a href=/>Go Back</a>", 403
    else:
        return "<h1>Bad Request</h1>", 400




# Call configure_app to set the base URL when the app is created


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)


