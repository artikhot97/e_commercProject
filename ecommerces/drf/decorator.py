

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from functools import wraps
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.authtoken.models import Token


def is_valid_token():
    def decorator(func):
        def wrap(request, *args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION', None)
            if not token:
                return HttpResponse("Token not exists", status=401)
            else:
                token = token.replace('Token ', '')
                try:
                    token_data = Token.objects.get(key=token)
                    if not token_data.user.is_active:
                        return HttpResponse("Unauthorized, Account Disabled", status=401)
                except Token.DoesNotExist:
                    return HttpResponse("Unauthorized", status=401)
            return func(request, *args, **kwargs)
        return wraps(func)(wrap)
    return decorator