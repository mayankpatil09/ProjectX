from ssh import connect_to_server, transfer_folder
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Global variable to store progress
progress = 0

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login_form')
def login_form():
    return render_template('login_form.html')


@app.route('/blank')
def blank():
    return render_template('blank.html')


@app.route('/process')
def process():
    return render_template('process.html')


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/submit_login', methods=['POST'])
def submit_form1():
    global ssh_client

    host = request.form.get('host')
    port = int(request.form.get('port'))
    username = request.form.get('username')
    password = request.form.get('password')
    keyfile = request.files.get('keyfile')

    keyfile_path = None
    if keyfile:
        keyfile_path = os.path.join('uploads', keyfile.filename)
        keyfile.save(keyfile_path)

    # Ensure connect_to_server returns a tuple
    ssh_client, current_directory, message = connect_to_server(host, port, username, password, keyfile_path)
    
    if ssh_client:
        session['ssh_client'] = json.dumps({
            'host': host,
            'port': port,
            'username': username,
            'password': password,
            'keyfile_path': keyfile_path
        })
        return render_template('result.html', 
                               connection_message=message, 
                               current_directory=current_directory,
                               host=host, 
                               port=port, 
                               username=username, 
                               password=password, 
                               keyfile_path=keyfile_path)
    else:
        return render_template('error.html', connection_message=f"An error occurred: {message}", current_directory=None)

@app.route('/transfer_folder', methods=['POST'])
def transfer_folder_route():
    global progress
    progress = 0  # Reset progress at the start

    if 'ssh_client' not in session:
        return redirect(url_for('form1'))

    ssh_client_data = json.loads(session['ssh_client'])
    host = ssh_client_data['host']
    port = ssh_client_data['port']
    username = ssh_client_data['username']
    password = ssh_client_data['password']
    keyfile_path = ssh_client_data.get('keyfile_path')

    local_path = request.form.get('local_path')
    original_folder = request.form.get('original_folder')

    try:
        ssh, current_directory, message = connect_to_server(host, port, username, password, keyfile_path)
        
        if ssh:
            transfer_result = transfer_folder(ssh, local_path, os.path.dirname(original_folder), progress_callback=update_progress)
        else:
            transfer_result = f"Failed to connect: {message}"
    except Exception as e:
        transfer_result = f"Error during folder transfer: {str(e)}"

    return render_template('b.html', connection_message="Folder transfer completed")

def update_progress(filename, size, sent):
    global progress
    progress = round((sent / size) * 100)
    print(f"Progress: {progress}%")

@app.route('/progress')
def progress_route():
    global progress
    return jsonify(testint=progress)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
