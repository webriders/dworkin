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
        user = Variable(self.user_var).resolve(context)

        try:
            profile = user.get_profile()
        except:
            profile = None
            logger.warning("Can't get user profile")

        if profile:
            if profile.use_gravatar:
                import urllib, hashlib
                img_url = "http://www.gravatar.com/avatar/" + hashlib.md5(user.email.lower()).hexdigest() + "?"
                img_url += urllib.urlencode({ 'd': img_url, 's': str(self.size) })
            elif profile.avatar:
                img_url = profile.avatar.url
            else:
                img_url = DEFAULT_AVATAR_URLS[profile.gender or '']

        return u'<img src="%s" alt="%s" title="%s" width="%s" height="%s" />' % (img_url, user.username, user.get_full_name() or user.username, self.size, self.size)

register.tag(user_avatar)
