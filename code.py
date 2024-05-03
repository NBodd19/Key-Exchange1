import random
import math   
import hashlib

def isPrime(number):
  if number == 2:
      return True
  elif number % 2 == 0:
      return False
  sqrt = math.isqrt(number)
  return all(number % i != 0 for i in range(3, sqrt + 1, 2))

def genPrime():
    num = 4
    while not isPrime(num):
        num = random.randint(10, 100000)
    return num

def primRoot(prime):
    for i in range(2, prime):
        powers = []
        for j in range(1, prime):
            power = (i ** j) % prime
            if power in powers:
                break
            powers.append(power)
        if len(powers) == prime - 1:
            return i
    return None

def pTable(a, b, A, B, Sa, Sb, p):
    print("Alice     Bob     Eve")
    print(f"{str(a)}     {str(b)}     N/A")
    print(f"{str(A)}     {str(B)}     {str(A)} & {str(B)}")
    print(f"{str(Sa)}     {str(Sb)}     {str((A ** B) % p)}")

def encrypt(message, key):
    h = hashlib.sha256()
    h.update(str(key).encode())
    key = h.digest()
    print(f"key = {key}")
    key_length = len(key)
    encrypted_message = ""
    for i in range(0, len(message), key_length):
        chunk = message[i:i + key_length]
        for j in range(len(chunk)):
            encrypted_message += chr(ord(chunk[j]) ^ key[j])
    return encrypted_message

def decrypt(encry_m, key):
    h = hashlib.sha256()
    h.update(str(key).encode())
    key = h.digest()
    key_length = len(key)
    decry_message = ""
    for i in range(0, len(encry_m), key_length):
        chunk = encry_m[i:i + key_length]
        for j in range(len(chunk)):
            decry_message += chr(ord(chunk[j]) ^ key[j])
    return decry_message

def main():
    with open("message.txt", "r") as file:
      message = file.read()
    p = genPrime()
    g = primRoot(p)
    a = random.randint(1, p - 1)
    A = (g ** a) % p
    b = random.randint(1, p - 1)
    B = (g ** b) % p
    shared_secret_key_A = (B ** a) % p
    
    shared_secret_key_B = (A ** b) % p
    if shared_secret_key_A == shared_secret_key_B:
        print("Shared keys match")
    else:
        print("Shared keys don't match")
    encrypted_message = encrypt(message, shared_secret_key_A)
    with open("encrypted.txt", "w") as file1:
        file1.write(encrypted_message)
    decry_message = decrypt(encrypted_message, shared_secret_key_B)
    with open("decrypted.txt", "w") as file2:
        file2.write(decry_message)
    pTable(a, b, A, B, shared_secret_key_A, shared_secret_key_B, p)
    print(f"\nEncrypted message: {encrypted_message} \nDecrypted message: \n{decry_message}")
    

if __name__ == "__main__":
  main()