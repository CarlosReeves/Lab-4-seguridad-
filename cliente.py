import socket
import random

def receive_key(conn):
    key_str = conn.recv(4096).decode()
    n, e = map(int, key_str.split(','))
    return n, e

def generate_private_key(public_key, phi):
    # Generar la clave privada usando la clave pública recibida y phi
    n, e = public_key
    d = mod_inverse(e, phi)
    return n, d

def send_encrypted_message(conn, message, public_key):
    n, e = public_key
    encrypted_message = ','.join([str(pow(ord(char), e, n)) for char in message])
    conn.sendall(encrypted_message.encode())

def receive_encrypted_message(conn, private_key):
    encrypted_message = conn.recv(4096).decode()
    n, d = private_key
    decrypted_message = ''.join([chr(pow(int(char), d, n)) for char in encrypted_message.split(',')])
    return decrypted_message

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    public_key = receive_key(client_socket)
    phi = (public_key[0] - 1) * (public_key[1] - 1)

    message = "Hola, servidor. Este es un mensaje cifrado."
    print(f"Mensaje original: {message}")

    private_key = generate_private_key(public_key, phi)
    send_encrypted_message(client_socket, message, public_key)

    decrypted_message = receive_encrypted_message(client_socket, private_key)
    print(f"Mensaje cifrado: {decrypted_message}")

    client_socket.close()

if __name__ == "__main__":
    main()
