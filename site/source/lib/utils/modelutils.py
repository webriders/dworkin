#!/usr/bin/python
# -*- coding: UTF-8 -*-


def create_linked_models_html(objects, app_name, model_name):
    """Create html list from given model objects. Can be used to show linked objects in the django admin object list.
    Example: we have Plant objects and each plant have plenty of Feature objects.
    You pass feature objects to this function and will get:
    <ul>
        <li> <a href="link for Feature editing"> Feature 1 </a></li>
        <li> <a href="link for Feature editing"> Feature 2 </a></li>
        <li> <a href="link for Feature editing"> Feature 3 </a></li>
        <li> <a class="addlink" href="link to add new Feature">Add</a> </li>
    </ul>
    """
    rs = objects
    ret = ''
    for obj in objects:
        ret += u"""<li><a href="/admin/%s/%s/%d/">%s</a></li>""" % (app_name, model_name, obj.id, unicode(obj))
    return u"""<ul>%s
            <li>
                <a class="addlink" href="/admin/%s/%s/add/">Add</a>
            </li>
        </ul>""" % (ret, app_name, model_name)

def create_img_html(title, link):
    """Create html image"""
    return '<img title="%s" alt="%s" src="%s" />' % (title, title, link)
