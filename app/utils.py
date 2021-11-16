from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashing Function
def hash(password : str):
    """This function will take a plain text password and will return a hashed password"""
    return pwd_context.hash(password)

# Function to compare plain password to hashed password
def verify_password(plain_password, hashed_password):
    """This function will hash the plain password and compare with the hashed password"""
    return pwd_context.verify(plain_password, hashed_password)