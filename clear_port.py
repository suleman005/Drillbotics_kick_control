import socket

def clear_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('localhost', port))
    except OSError:
        # Port is already in use
        sock.close()
        print(f"Port {port} is already in use and has been cleared.")
    else:
        # Port is available
        sock.close()
        print(f"Port {port} is available.")

# Specify the port you want to clear
port_to_clear = 3050

# Clear the port
clear_port(port_to_clear)
