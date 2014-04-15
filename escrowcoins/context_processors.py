from django.conf import settings


def global_vars(request):
    LOGGED_IN = False
    if request.user.is_authenticated():
        LOGGED_IN = True
    ga_prop_id = settings.GOOGLE_ANALYTICS_PROPERTY_ID
    ga_domain = settings.GOOGLE_ANALYTICS_DOMAIN
    return{'APP_NAME': settings.APP_NAME,'BASE_URL':settings.BASE_URL,
    'LOGGED_IN':LOGGED_IN,
    'GOOGLE_ANALYTICS_PROPERTY_ID':ga_prop_id,
    'GOOGLE_ANALYTICS_DOMAIN':ga_domain,
    'DEBUG':settings.DEBUG}
