from django.conf import settings
import datetime
import utils

class timeOutMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            if 'lastRequest' in request.session:            
                elapsedTime = datetime.datetime.now() - \
                 request.session['lastRequest']
                if elapsedTime.seconds > 15*60:
                    del request.session['lastRequest'] 
                    logout(request)
            request.session['lastRequest'] = datetime.datetime.now().isoformat()
        else:
            if 'lastRequest' in request.session:
                del request.session['lastRequest'] 

        return None