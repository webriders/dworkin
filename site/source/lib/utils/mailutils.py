from django.conf import settings
from django.template.loader import get_template
from django.template.context import Context
from django.core import mail

def mail_users(users, subject, template, params):
    ''' -  '''
    try:
        template = get_template(template)
        body = template.render(Context(params))

        connection = mail.get_connection()
        connection.open()

        messages = []
        for u in users:
            email = u.username
            if settings.DEBUG:
                email = "info@webriders.com.ua"

            msg = mail.EmailMessage(
                subject= settings.EMAIL_SUBJECT_PREFIX + subject,
                body=body,
                to=["%s <%s>" % (u.get_full_name(), email)])
            msg.content_subtype = "html"
            messages.append(msg)

        # notify managers also
        msg = mail.EmailMessage(
                subject= settings.EMAIL_SUBJECT_PREFIX + " [For admins] " + subject,
                body=body,
                to=["andrey.sokolov@webriders.com.ua"])
        msg.content_subtype = "html"  # Main content is now text/html
        messages.append(msg)

        connection.send_messages(messages)
        connection.close()
    except Exception, e:
        print str(e)
