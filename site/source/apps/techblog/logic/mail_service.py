# -*- encoding:utf-8 -*-

from utils.mail_utils import mail_users
from django.contrib.sites.models import Site


class MailService(object):

    @staticmethod
    def send_mail_on_user_activate(request, user):
        mail_users(
            [],
            u"Пользователь %s активирован" % user,
            "mail/mail_user_activate.html",
            {
                "site_url": Site.objects.get_current(),
                "user": user,
            }
        )


    @staticmethod
    def send_mail_on_article_publish(article, user):
        mail_users(
            [],
            u"Пользователь %s опубликовал статью" % user,
            "mail/mail_article_publish.html",
            {
                "site_url": Site.objects.get_current(),
                "article": article,
                "user": user,
            }
        )


    @staticmethod
    def send_mail_on_article_unpublish(article, user):
        mail_users(
            [],
            u"Пользователь %s скрыл статью" % user,
            "mail/mail_article_unpublish.html",
            {
                "site_url": Site.objects.get_current(),
                "article": article,
                "user": user,
            }
        )

    @staticmethod
    def send_mail_on_article_comment(comment):
            mail_users(
            [],
            u"Новый комментарий от пользователя %s: " % comment.user,
            "mail/mail_article_comment.html",
            {
                "site_url": Site.objects.get_current(),
                "comment": comment,
            }
        )
