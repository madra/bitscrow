'''
Decorators
'''
from django.shortcuts import Http404

from django.contrib import messages


def logged_out_required(function):
    '''This method cannot be used if a user is logged'''
    def wrapper(request, *args, **kw):
        if request.user and request.user.is_authenticated():
            messages.error(request, 'You cannot access this page')
            raise Http404
        else:
            return function(request, *args, **kw)
    return wrapper