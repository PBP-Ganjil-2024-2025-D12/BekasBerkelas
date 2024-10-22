from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from jwt import InvalidTokenError

class JWTAuthenticationMiddleware:
    def __init__(self, get_response) :
        self.get_response = get_response
        
    def __call__(self, request) :
        request.user = AnonymousUser()
        token = request.COOKIES.get('access_token')
        
        if token :
            try :
                decoded_token = AccessToken(token)
                User = get_user_model()
                
                try :
                    user = User.object.select_related('userprofile').get(id=decoded_token['user_id'])
                    request.user = user
                    request.user_role = user.userprofile.role
                except User.userprofile.RelatedObjectDoesNotExist :
                    pass
                    
            except (InvalidTokenError, User.DoesNotExist) :
                pass
        response = self.get_response(request)
        return response