import socket
import random

def receive_key(conn):
    key_str = conn.recv(4096).decode()
    p, g, y = map(int, key_str.split(','))
    return p, g, y

def generate_private_key(p):
    return random.randint(1, p - 2)

def send_encrypted_message(conn, message, public_key):
    p, g, y = public_key
    k = random.randint(1, p - 2)
    a = mod_pow(g, k, p)
    b = (mod_pow(y, k, p) * message) % p
    encrypted_message = f"{a},{b}"
    conn.sendall(encrypted_message.encode())

def receive_encrypted_message(conn, private_key, public_key):
    p, _, _ = public_key
    a, b = map(int, conn.recv(4096).decode().split(','))
    s = mod_pow(a, private_key, p)
    decrypted_message = (b * mod_pow(s, p - 2, p)) % p
    return decrypted_message

def mod_pow(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    public_key = receive_key(client_socket)
    private_key = generate_private_key(public_key[0])

    original_message = 42  # El mensaje debe ser un número entero en este caso
    print(f"Mensaje original: {original_message}")

    send_encrypted_message(client_socket, original_message, public_key)
    print("Mensaje cifrado enviado al servidor.")

    decrypted_message = receive_encrypted_message(client_socket, private_key, public_key)
    print(f"Mensaje descifrado: {decrypted_message}")

    client_socket.close()

if __name__ == "__main__":
    main()
