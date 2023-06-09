from rest_framework_simplejwt.tokens import RefreshToken

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