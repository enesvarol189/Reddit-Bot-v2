from flask import Flask, request
import subprocess
import requests
import os

app = Flask(__name__)

@app.route('/check_bot', methods=['POST'])
def check_bot():
    process = "Plant_Clinic_Bot"
    try:
        output = subprocess.check_output(f"pgrep -f {process}", shell=True)
    except subprocess.CalledProcessError:
        requestor = request.remote_addr
        port = request.headers.get('Client-Port')
        requests.post(f'http://{requestor}:{port}', data={'message': f'{process} has stopped'})
        return f'{process} has stopped', 200
    return f'{process} is running', 200

@app.route('/start_bot', methods=['GET'])
def start_bot():
    os.chdir('Plant_Clinic_Bot')
    subprocess.Popen(["python", "main.py", "start"])
    return 'Bot started', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))