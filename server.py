import socket
import random

def generate_key_pair():
    p = generate_prime_number()
    q = generate_prime_number()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = select_public_key(phi)
    d = mod_inverse(e, phi)
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key

def generate_prime_number():
    while True:
        num = random.randint(100, 500)
        if is_prime(num):
            return num

def is_prime(num):
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def select_public_key(phi):
    while True:
        e = random.randint(2, phi - 1)
        if gcd(e, phi) == 1:
            return e

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def send_key(conn, key):
    n, e = key
    key_str = f"{n},{e}"
    conn.sendall(key_str.encode())

def receive_encrypted_message(conn, private_key):
    encrypted_message = conn.recv(4096).decode()
    n, d = private_key
    decrypted_message = ''.join([chr(pow(int(char), d, n)) for char in encrypted_message.split(',')])
    return decrypted_message

def send_encrypted_message(conn, message, public_key):
    n, e = public_key
    encrypted_message = ','.join([str(pow(ord(char), e, n)) for char in message])
    conn.sendall(encrypted_message.encode())

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)

    print("Esperando conexión...")
    conn, addr = server_socket.accept()
    print(f"Conectado a {addr}")

    public_key, private_key = generate_key_pair()
    send_key(conn, public_key)

    message = "Hola, cliente."
    print(f"Mensaje recibido: {message}")

    send_encrypted_message(conn, message, public_key)

    decrypted_message = receive_encrypted_message(conn, private_key)
    print(f"Mensaje descifrado: {decrypted_message}")

    conn.close()

if __name__ == "__main__":
    main()
