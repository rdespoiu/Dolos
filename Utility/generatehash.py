import hashlib, uuid

def generateHash(salt, inp):
    hashedInput = hashlib.sha512(inp + salt).hexdigest()
    return hashedInput

def generateSalt():
    return uuid.uuid4().hex
