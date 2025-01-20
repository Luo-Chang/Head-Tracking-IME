import socket
import struct
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# Define the IP and port to listen on
UDP_IP = config["udp"]["UDP_IP"]
UDP_PORT = config["udp"]["UDP_PORT"]

# Define the structure format for four double-precision floats
FORMAT = "dddddd"  # 6 doubles (each double is 8 bytes)
BUFFER_SIZE = struct.calcsize(FORMAT)  # Calculate the size of the buffer

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the specified IP and port
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}...")

while True:
    try:
        # Receive data from the socket
        data, addr = sock.recvfrom(BUFFER_SIZE)

        # Unpack the received binary data into four doubles
        numbers = struct.unpack(FORMAT, data)

        # Print the received numbers
        print(f"Received from {addr}: {numbers}")

    except struct.error:
        print("Received data does not match the expected format.")
    except KeyboardInterrupt:
        print("\nShutting down the server.")
        break

# Close the socket
sock.close()
