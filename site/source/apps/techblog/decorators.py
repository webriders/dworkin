from website.models import *
from lib.utils.log import logger
from datetime import datetime, timedelta

'''
This is the place for decorators used in views
'''

def decorate_params_add_info(f):
    # New decorated function
    def wrapped(request, *args, **kwds):
        # Init params
        params = kwds.get('params', {})

        info = Info.objects.all()
        if (len(info) == 0):
            logger.error("Info is empty!!!")
        elif (len(info) > 1):
            logger.error("Info contains more than one record!!!")
            params["info"] = info[0]
        else:
            params["info"] = info[0]

        kwds['params'] = params
        # Execute original function
        return f(request, *args, **kwds)

    return wrapped

def decorate_params_add_residents(f):
    # New decorated function
    def wrapped(request, *args, **kwds):
        # Init params
#        params = kwds.get('params', {})
#        residents = params["residents"] = Resident.objects.all()
#
#        resident_id = request.GET.get('resident_id') or request.COOKIES.get('resident_id')
#        in_cookie = 'resident_id' in request.COOKIES
#
#        resident = None
#        try:
#            resident = residents.filter(id=int(resident_id))
#            if 'resident_id' in request.GET:
#                in_cookie = False # we have resident_id in request.GET, it's correct, we should store it in COOKIES
#        except:
#            in_cookie = False # stored in COOKIES resident ID was wrong. We should re-store it
#            if len(residents):
#                resident = [residents[0]]
#
#        if resident:
#            resident = resident[0]
#            params["resident"] = resident
#            params["residents"] = params["residents"].exclude(id=resident.id)
#
#        kwds['params'] = params
#
#        # Execute original function
        response = f(request, *args, **kwds)
#
#        # Set new resident id to cookies (if it's not presented yet)
#        if not in_cookie and resident:
#            response.set_cookie('resident_id', resident.id, path = "/")
#        response.set_cookie('language', request.LANGUAGE_CODE, path = "/")

        return response

    return wrapped