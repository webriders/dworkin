#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Global project constants
'''

PAGE_TEMPLATES_PATH = 'page/%s'
GENDER_MALE = 'male'
GENDER_FEMALE = 'female'
DEFAULT_AVATAR_URLS = {
    '': '/static/techblog/img/common/users/unknown_%s.png',
    GENDER_MALE: '/static/techblog/img/common/users/man_%s.png',
    GENDER_FEMALE: '/static/techblog/img/common/users/lady_%s.png',
}