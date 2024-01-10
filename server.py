import os
import socket
import json
import sys
import threading
import importlib


def client_handler(conn, addr, is_last, next_server_addr, server_id, control_ip, control_port, start_layer, end_layer):
    try:
        data = b""
        while True:
            part = conn.recv(4096)
            if not part:
                break
            data += part

        if not data:
            print(f"No data received from {addr}")
            return

        try:
            message = json.loads(data.decode())

        
            inferenceResult = module.predict(model, start_layer, end_layer)

            
            if(isinstance(inferenceResult, module.torch.Tensor)):
                inferenceResult=inferenceResult.tolist()
            message['message'] = 0
            #print(f"Processed result from {server_id}: {inferenceResult}")

            # Forward or return the processed message
            if is_last:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as return_socket:
                    return_socket.connect((message['returnIP'], message['returnPort']))
                    return_socket.sendall(json.dumps(message).encode())
            else:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as forward_socket:
                    forward_socket.connect(next_server_addr)
                    forward_socket.sendall(json.dumps(message).encode())

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {addr}: {e}")
            print(f"Received data: {data.decode()[:1000]}")

    except Exception as e:
        print(f"Server.py Error: Exception handling connection from {addr}: {e}")
    finally:
        conn.close()

def start_server(in_port, is_last, control_ip, control_port, next_server_ip=None, next_server_port=None, start_layer=0, end_layer=None):
    server_id = f"Server_{in_port}"
    next_server_addr = (next_server_ip, next_server_port) if next_server_ip else None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("10.0.0.17", in_port))
        s.listen()
        print(f"{server_id} listening on port {in_port}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=client_handler, args=(conn, addr, is_last, next_server_addr, server_id, control_ip, control_port, start_layer, end_layer))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":

    #PULL FROM CONFIG FILE


    # Parse command-line arguments
    netName = sys.argv[1]
    startLayer = int(sys.argv[2])
    endLayer = int(sys.argv[3])
    listenPort = int(sys.argv[4])
    nextIP = None if sys.argv[5] == 'None' else sys.argv[5]
    nextPort = None if sys.argv[6] == 'None' else int(sys.argv[6])

    control_ip = '127.0.0.1'  # Replace with actual control IP
    control_port = 1026       # Replace with actual control port
    is_last = nextPort == 'None'

   # Path to the directory containing all virtual environments
    venv_base_path = '/home/austin/venv/'

    # Construct the path to the site-packages of the virtual environment
    venv_site_packages = os.path.join(venv_base_path, netName, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages')

    # Add this path to sys.path
    sys.path.insert(0, venv_site_packages)

    # Now import the modules that are installed in the virtual environment
    module = importlib.import_module(netName)
    model = module.getModel()



    start_server(listenPort, is_last, control_ip, control_port, nextIP, nextPort, startLayer, endLayer)
