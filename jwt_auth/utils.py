from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

def set_jwt_cookies(response, user) :
    refresh = RefreshToken.for_user(user)
    refresh['role'] = user.userprofile.role
    refresh['name'] = user.userprofile.name
    
    response.set_cookie(
        'access_token',
        str(refresh.access_token),
        max_age = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME').total_seconds(),
        httponly=True,
        samesite='Lax',
        secure=settings.JWT_COOKIE_SECURE
    )
    
    response.set_cookie(
        'refresh_token',
        str(refresh),
        max_age=settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME').total_seconds(),
        httponly=True,
        samesite='Lax',
        secure=settings.JWT_COOKIE_SECURE
    )
    
    return response

def clear_jwt_cookies(response) :
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response