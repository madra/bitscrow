'''
utility functions
'''
import settings
import requests
from django.http import HttpResponseNotFound ,Http404
from django.contrib import messages

def send_simple_message(to,sender,message,subject):
    '''
    mailgun
    '''
    response = requests.post(
        #"https://api.mailgun.net/v2/samples.mailgun.org/messages",
        settings.MAILGUN_ACCESS_LINK,
        auth=("api",settings.MAILGUN_ACCESS_KEY),
        data={"from": sender,
              "to": to,
              "subject": subject,
              "text": message})
    return response.status_code


def default(obj):
    """Default JSON serializer."""
    import calendar, datetime
    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    millis = int(
        calendar.timegm(obj.timetuple()) * 1000 +
        obj.microsecond / 1000
    )
    return millis



def logged_out_required(function):
    '''This method cannot be used if a user is logged'''
    def wrapper(request, *args, **kw):
        if request.user and request.user.is_authenticated():
            messages.error(request, 'You cannot access this page')
            raise Http404
        else:
            return function(request, *args, **kw)
    return wrapper