import paramiko
import os
import datetime
import time
from scp import SCPClient

def connect_to_server(host, port, username, password, keyfile_path=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if keyfile_path and os.path.exists(keyfile_path):
            private_key = paramiko.RSAKey.from_private_key_file(keyfile_path)
            ssh.connect(host, port=port, username=username, pkey=private_key, disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})
        else:
            ssh.connect(host, port=port, username=username, password=password)

        time.sleep(2)
        print(f'Connected to {host} as {username}')

        # Get the current working directory
        stdin, stdout, stderr = ssh.exec_command('pwd')
        current_directory = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Error getting current directory: {error}")
            return None, None, f"Error: {error}"
        else:
            print(f"Current working directory on remote server: {current_directory}")
            return ssh, current_directory, f"Connected to {host} as {username}"

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, str(e)

def transfer_folder(ssh, local_path, remote_folder, progress_callback=None):
    """Transfer a folder from local to the remote server and rename it with a timestamp."""
    
    def create_scp_client(ssh_client):
        """Create and return an SCP client."""
        return SCPClient(ssh_client.get_transport(), progress=progress_callback)

    if not os.path.exists(local_path):
        raise FileNotFoundError(f"The local path '{local_path}' does not exist.")
    
    if os.path.isdir(local_path):
        # Define the remote path where the folder will be copied
        remote_path = os.path.join(remote_folder, os.path.basename(local_path)).replace('\\', '/')
        print(f"Copying folder to: {remote_path}")

        # Transfer the folder
        with create_scp_client(ssh) as scp:
            scp.put(local_path, remote_path, recursive=True)
        
        print(f"Folder '{local_path}' copied to '{remote_path}'")

        # Generate the new name with timestamp
        current_date = datetime.datetime.now().strftime("%d%b%Y")
        current_time = datetime.datetime.now().strftime("%H-%M")
        new_folder_name = f"Installer_{current_date}_{current_time}"
        new_remote_path = os.path.join(remote_folder, new_folder_name).replace('\\', '/')

        # Rename the remote folder
        rename_command = f'mv "{remote_path}" "{new_remote_path}"'
        stdin, stdout, stderr = ssh.exec_command(rename_command)
        error = stderr.read().decode().strip()

        if error:
            print(f"Error renaming folder: {error}")
            return f"Error renaming folder: {error}"
        else:
            print(f"Folder renamed to '{new_remote_path}'")
            return f"Folder transferred and renamed to '{new_remote_path}'"
    else:
        raise ValueError("The specified path is not a directory.")
