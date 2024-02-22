from Crypto.Cipher import AES
import hashlib

def local_api_encrypt(src, sn):
    key = ("$<^&;:|~`?" + sn).encode('utf-8')
    iv = bytes([184, 71, 97, 125, 200, 53, 61, 10, 34, 110, 174, 54, 18, 118, 117, 226])

    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    src_len = len(src)
    padded_len = (src_len + AES.block_size - 1) // AES.block_size * AES.block_size
    padded_src = src.ljust(padded_len, b'\0')
    
    ciphertext = cipher.encrypt(padded_src)

    return ciphertext

def local_api_decrypt(ciphertext, sn):
    key = ("$<^&;:|~`?" + sn).encode('utf-8')
    iv = bytes([184, 71, 97, 125, 200, 53, 61, 10, 34, 110, 174, 54, 18, 118, 117, 226])

    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    decrypted = cipher.decrypt(ciphertext)
    
    return decrypted.rstrip(b'\0')



if __name__ == "__main__":
    serial_number = "AA-70-2012-01-0116-176"

    # Unit test
    # plaintext = b"{\"Cmd\":101,\"DevCode\":\"\",\"Time\":1693386965,\"Model\":\"PNZ-UN0\",\"DevSN\":\"AA-70-2012-01-0116-176\",\"Timezone\":-8,\"IP\":\"192.168.10.112\",\"Vendor\":\"Noonspare\",\"Token\":\"2tzdw9rd2Nff3tnai42Q2c7dzM/S09Py\"}"
    plaintext = ("{\"IP\":\"192.168.10.112\",\"DevSN\":\"%s\"}" % serial_number).encode("utf-8")
    print(f"Plain text length: {plaintext.__len__()}")
    print(f"Plain text: {plaintext.decode()}")


    encrypted_data = local_api_encrypt(plaintext, serial_number)
    print(f"Encrypted length: {encrypted_data.__len__()}")
    print(f"Encrypted: {encrypted_data.hex()}")

    decrypted_data = local_api_decrypt(encrypted_data, serial_number)
    print(f"Decrypted length: {decrypted_data.__len__()}")
    print(f"Decrypted: {decrypted_data.decode()}")
