from Crypto.PublicKey import RSA

def generate_public_and_private_key(bit=3072):
    keyPair = RSA.generate(bit)
    pubKey = keyPair.publickey()
    pubKeyPEM = pubKey.exportKey()
    privKeyPEM = keyPair.exportKey()
    
    return pubKeyPEM.decode()[27:-25], privKeyPEM.decode()[32:-30]