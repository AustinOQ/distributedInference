import socket
import sys
import json
import time


def receive_message(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('10.0.0.17', port))
        s.listen()
        print(f"Listening for messages on port {port}")
        
        while True:
            conn, _ = s.accept()
            with conn:
                data = b""
                while True:
                    part = conn.recv(4096)  # Use a larger buffer size
                    data += part
                    if len(part) < 4096:  # If less data is received, it's likely the end of the message
                        break
                if not data:
                    print("No data received.")
                    continue

                try:
                    message = json.loads(data.decode())
                    current_time = time.time()
                    elapsed_time = current_time - message['start_time']
                    print(f"Recieved!")

                    # Write latency to a file
                    with open("OneDevice0-3NoSplit.txt", "a") as file:
                        file.write(f"{elapsed_time}\n")

                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
                    print(f"Received data (truncated): {data[:200]}...")  # Only show the first 200 chars

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 client_receive.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    receive_message(port)
