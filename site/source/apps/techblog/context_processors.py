import constants


def add_constants(request):
    context = {}
    for cn in dir(constants):
        if cn.isupper():
            context[cn] = getattr(constants, cn)
    return context


#''' This is map processing '''
## Demo key is valid for all webriders.com.ua and all its sub-domains
#YANDEX_MAP_KEY_DEMO = 'ANXwg0sBAAAA_TRxWwMALTsauyfMKj5heb4Q-DnPIXsze3kAAAAAAAAAAAB9yKWtVno1qTyHKZYsk5hRDr2YJQ=='
## Production key is valid for obriens.kiev.ua and all its sub-domains
#YANDEX_MAP_KEY_PROD = 'AN0SiEsBAAAAlrioAQMA9v0wt_1UvprqkITX2DXhl-yRrisAAAAAAAAAAADfO2lwmkYPvxSXfkN-G7zioKmMqA=='
#
## Demo key is valid for all webriders.com.ua and all its sub-domains
#GOOGLE_MAP_KEY_DEMO = 'ABQIAAAAHiFvnyWDhk1oAcIFMBOkCxT_1dKf7KYw9czw7zEt2eVcgprgLBSXla6ACvQG-Ss7bOEz_YOajS6ffg'
## Production key is valid for obriens.kiev.ua and all its sub-domains
#GOOGLE_MAP_KEY_PROD = 'ABQIAAAAHiFvnyWDhk1oAcIFMBOkCxS9CVOSrbCo-ilgTAav81qorBLN-hRr_h42eSb34ljqRKXbFFAyfU3taA'
#
#def add_maps_key(request):
#    yandex_key = YANDEX_MAP_KEY_DEMO
#    google_key = GOOGLE_MAP_KEY_DEMO
#    if request.get_host() in 'www.obriens.kiev.ua':
#        yandex_key = YANDEX_MAP_KEY_PROD
#        google_key = GOOGLE_MAP_KEY_PROD
#    return { 'yandex_maps_key': yandex_key, 'google_maps_key': google_key }


#def add_site_mode(request):
#    key = 'dev'
#    if request.get_host() in 'www.obriens.kiev.ua':
#        key = 'prod'
#    if request.get_host() in 'www.obriens.webriders.com.ua':
#        key = 'demo'
#    return { 'site_mode': key }

