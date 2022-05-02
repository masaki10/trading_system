from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_data(key, data, filename):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(filename, "wb") as f:
        f.write(key)
        f.write(cipher.nonce)
    return ciphertext, tag

def decrypt_data(key, ciphertext, tag, filename):
    with open(filename, "rb") as f:
        k = f.read(16)
        nonce = f.read(16)
    cipher_dec = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher_dec.decrypt_and_verify(ciphertext, tag)
    return data

if __name__ == "__main__":
    key = get_random_bytes(16)

    pwd_ctxt, pwd_tag = encrypt_data(key, b"masha1003", "../pwd_key.bin")
    print("pwd")
    print(pwd_ctxt)
    print(pwd_tag)

    order_num_ctxt, order_num_tag = encrypt_data(key, b"2625", "../order_num_key.bin")
    print("order_num")
    print(order_num_ctxt)
    print(order_num_tag)

    print("============test=============")
    data = decrypt_data(key, pwd_ctxt, pwd_tag, "../pwd_key.bin")
    print(data)
    data = decrypt_data(key, order_num_ctxt, order_num_tag, "../order_num_key.bin")
    print(data)