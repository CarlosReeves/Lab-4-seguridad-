import socket
import random

def mod_pow(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

def generate_key_pair():
    # Generar claves ElGamal (p, g, x)
    p = generate_prime_number()
    g = random.randint(2, p - 2)
    x = random.randint(1, p - 2)
    y = mod_pow(g, x, p)
    public_key = (p, g, y)
    private_key = x
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

def send_key(conn, key):
    p, g, y = key
    key_str = f"{p},{g},{y}"
    conn.sendall(key_str.encode())

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

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)

    print("Esperando conexión...")
    conn, addr = server_socket.accept()
    print(f"Conectado a {addr}")

    public_key, private_key = generate_key_pair()
    send_key(conn, public_key)

    original_message = 42  # El mensaje debe ser un entero en este caso
    print(f"Mensaje original: {original_message}")

    send_encrypted_message(conn, original_message, public_key)
    print("Mensaje cifrado enviado al cliente.")

    decrypted_message = receive_encrypted_message(conn, private_key, public_key)
    print(f"Mensaje descifrado: {decrypted_message}")

    conn.close()

if __name__ == "__main__":
    main()
