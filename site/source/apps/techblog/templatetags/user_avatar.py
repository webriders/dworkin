from django import template
from django.template import Variable
from techblog.constants import DEFAULT_AVATAR_URLS
from lib.utils.log import logger

register = template.Library()

def user_avatar(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        params = token.split_contents()
        tag_name = params[0] # tag_name: "avatar"
        user_var = params[1] # user_var: User instance
        size = '64' # avatar size
        if len(params) == 3:
            size = params[2]
        elif len(params) > 2:
            raise IndexError
    except IndexError:
        raise template.TemplateSyntaxError, "%r tag requires 1 or 2 arguments" % token.contents.split()[0]
    return AvatarNode(tag_name, user_var, size)

class AvatarNode(template.Node):
    def __init__(self, tag_name, user_var, size):
        self.tag_name = tag_name
        self.user_var = user_var
        self.size = size

    def render(self, context):
        img_url = ''

        avatar_var = '%s.get_profile.avatar' % self.user_var
        fb_version = '"square%s"' % self.size
        user = Variable(self.user_var).resolve(context)

        try:
            default_img_url = DEFAULT_AVATAR_URLS[user.get_profile().gender] % self.size
        except:
            logger.warning("Can't get default avatar thumbnail for %s: no profile or gender is wrong (not in %s)" % (user, DEFAULT_AVATAR_URLS.keys()))
            default_img_url = DEFAULT_AVATAR_URLS[''] % self.size

        profile = user.get_profile()

        if profile and profile.use_gravatar:
            # import code for encoding urls and generating md5 hashes
            import urllib, hashlib

            # Set your variables here
            email = user.email
            size = self.size

            # construct the url
            img_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
            img_url += urllib.urlencode({ 'd': default_img_url, 's': str(size) })
        else:
            try:
                avatar = profile.avatar
                if not avatar:
                    raise
                from filebrowser.templatetags.fb_versions import VersionNode
                thumb_node = VersionNode(avatar_var, fb_version)
                img_url = thumb_node.render(context)
            except:
                logger.warning("Can't get avatar thumbnail for %s: no profile, no avatar or no django-filebrowser" % user)
                img_url = default_img_url

        return u'<img src="%s" alt="%s" title="%s" width="%s" height="%s" />' % (img_url, user.username, user.get_full_name() or user.username, self.size, self.size)

register.tag(user_avatar)
