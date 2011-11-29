# -*- encoding:utf-8 -*-

from utils.mailutils import mail_users
from django.contrib.sites.models import Site


class MailService(object):

    @staticmethod
    def send_mail_on_user_activate(request, user):
        mail_users(
            [],
            u"User '%s' have been activated" % user,
            "mail/mail_user_activate.html",
            {
                "site_url": Site.objects.get_current(),
                "user": user,
            }
        )


    @staticmethod
    def send_mail_on_first_article_publish(article, user):
        if not article.notified_on_first_publish:
            mail_users(
                [],
                u"User '%s' published the article" % user,
                "mail/mail_article_publish.html",
                {
                    "site_url": Site.objects.get_current(),
                    "article": article,
                    "user": user,
                }
            )

            article.notified_on_first_publish = True
            article.save()

    @staticmethod
    def send_mail_on_article_comment(comment):
            mail_users(
            [],
            u"New comment from user '%s': " % comment.user,
            "mail/mail_article_comment.html",
            {
                "site_url": Site.objects.get_current(),
                "comment": comment,
            }
        )
