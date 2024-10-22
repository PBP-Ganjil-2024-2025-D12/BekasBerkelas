from django.shortcuts import render
from jwt_auth.decorators import jwt_required, admin_required, seller_required, buyer_required
# Create your views here.

def main(request):
    return render(request, 'main.html')