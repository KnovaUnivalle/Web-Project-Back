from rest_framework_simplejwt.tokens import RefreshToken
import random
import string

def generateToke(user, rol):
    # Generate token for user using JWT
    refresh = RefreshToken.for_user(user)
    refresh['rol_id'] = rol
    data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'rol_id': rol
    }
    return data

def generate_random_password():
    length = random.randint(9, 15) 
    characters = string.ascii_letters + string.digits + string.punctuation

    while True:
        password = ''.join(random.choices(characters, k=length))

        if (any(char.islower() for char in password) and
            any(char.isupper() for char in password) and
            any(char.isdigit() for char in password) and
            any(char not in '`,:;"|~' for char in password)):
            return password