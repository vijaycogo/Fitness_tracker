from passlib.context import CryptContext

# Creating a CryptContext object for password hashing
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Creating a Hash class to handle password hashing and verification
class Hash():
    # Method to hash a password using bcrypt algorithm
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
    # Method to verify a plain password against its hashed counterpart.
    def verify(hashed_password,plain_password):
        return pwd_cxt.verify(plain_password,hashed_password)