import socket
import json
import sys
import threading
import time

def process_message(original_message, start_time, server_id):
    elapsed_time = time.time() - start_time
    original_message += f" - processed by {server_id} in {elapsed_time:.2f} seconds"
    return original_message

def notify_control_of_completion(command_used, control_ip, control_port):
    message = {
        'source': 'worker',
        'event': 'completed_request',
        'message': command_used,
    }
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((control_ip, control_port))
        sock.sendall(json.dumps(message).encode('utf-8'))
        print(f"Notification sent to control: {message}")

def client_handler(conn, addr, is_last, next_server_addr, server_id, control_ip, control_port, command_used):
    time.sleep(3)
    try:
        data = conn.recv(1024)
        if not data:
            return

        message = json.loads(data.decode())
        processed_message = process_message(message['message'], message['start_time'], server_id)
        message['message'] = processed_message

        if is_last:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as return_socket:
                return_socket.connect((message['returnIP'], message['returnPort']))
                return_socket.sendall(json.dumps(message).encode())
            notify_control_of_completion(command_used, control_ip, control_port)
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as forward_socket:
                forward_socket.connect(next_server_addr)
                forward_socket.sendall(json.dumps(message).encode())

    except json.JSONDecodeError:
        print(f"Error decoding JSON from {addr}")
    except Exception as e:
        print(f"Exception handling connection from {addr}: {e}")
    finally:
        conn.close()

def start_server(in_port, is_last, control_ip, control_port, command_used, next_server_ip=None, next_server_port=None):
    server_id = f"Server_{in_port}"
    next_server_addr = (next_server_ip, next_server_port) if next_server_ip else None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', in_port))
        s.listen()
        print(f"{server_id} listening on port {in_port}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=client_handler, args=(conn, addr, is_last, next_server_addr, server_id, control_ip, control_port, command_used))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python3 server.py <in_port> <is_last> <control_ip> <control_port> <command_used> [<next_server_ip> <next_server_port>]")
        sys.exit(1)

    in_port = int(sys.argv[1])
    is_last = sys.argv[2].lower() == 'true'
    control_ip = sys.argv[3]
    control_port = int(sys.argv[4])
    command_used = sys.argv[5]
    next_server_ip = sys.argv[6] if len(sys.argv) > 6 else None
    next_server_port = int(sys.argv[7]) if len(sys.argv) > 7 else None

    start_server(in_port, is_last, control_ip, control_port, command_used, next_server_ip, next_server_port)
