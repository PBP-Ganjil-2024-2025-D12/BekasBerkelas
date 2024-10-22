from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework_simplejwt.tokens import AccessToken
from jwt import InvalidTokenError, ExpiredSignatureError
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

def jwt_required(redirect_url = None, allowed_roles = None) :
    """
    Cara Penggunaan
    @jwt_required # Default redirect ke /login
    @jwt_required('authentication:login') # Redirect ke /login
    @jwt_required(roles = ['ADM']) # Hanya Admin yang bisa akses
    @jwt_required(roles = ['ADM', 'BUY']) # Admin dan Buyer yang bisa akses
    @jwt_required(redirect_url='authentication:login', roles = ['ADM']) # Admin yang bisa akses dan redirect ke /login
    """
    
    if callable(redirect_url) :
        view_func = redirect_url
        redirect_url = 'authentication:login'
        return jwt_required(redirect_url)(view_func)
    
    if redirect_url is None :
        redirect_url = 'authentication:login'
        
    def decorator(view_func) :
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs) :
            access_token = request.COOKIES.get('access_token')
            
            if not access_token :
                messages.error(request, 'Please login to continue')
                return redirect(redirect_url)
            
            try :
                token = AccessToken(access_token)
                user_id = token['user_id']
                User = get_user_model()
                user = User.objects.select_related('userprofile').get(id=user_id)
                
                if allowed_roles :
                    try :
                        user_role = user.userprofile.role
                        if user_role not in allowed_roles :
                            messages.error(request, 'You don\'t have permission to access this page')
                            return redirect(redirect_url)
                    except ObjectDoesNotExist :
                        messages.error(request, 'User profile not found')
                        return redirect(redirect_url)
                    
                request.user = user
                return view_func(request, *args, **kwargs)
                
            except ExpiredSignatureError :
                messages.error(request, 'Session expired. Please login again')
                response = redirect(redirect_url)
                response.delete_cookie('access_token')
                response.delete_cookie('refresh_token')
                return response
            
            except (InvalidTokenError, User.DoesNotExist) :
                messages.error(request, 'Invalid session. Please login again')
                response = redirect(redirect_url)
                response.delete_cookie('access_token')
                response.delete_cookie('refresh_token')
                return response
            
        return wrapped_view
    return decorator

def admin_required(redirect_url='authentication:login'):
    return jwt_required(redirect_url=redirect_url, allowed_roles=['ADM'])

def seller_required(redirect_url='authentication:login'):
    return jwt_required(redirect_url=redirect_url, allowed_roles=['SEL'])

def buyer_required(redirect_url='authentication:login'):
    return jwt_required(redirect_url=redirect_url, allowed_roles=['BUY'])