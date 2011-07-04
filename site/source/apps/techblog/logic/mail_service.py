# -*- encoding:utf-8 -*-

from utils.mail_utils import mail_users

Profile = 0

class MailService(object):

    @staticmethod
    def send_mail_on_user_activate(request, user):
        mail_users(
            [],
            u"Пользователь %s активирован" % user,
            "mail/mail_user_activate.html",
            {
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
                "article": article,
                "user": user,
            }
        )



    @staticmethod
    def send_mail_on_article_comment(request, comment):
            mail_users(
            [],
            u"Новый комментарий от пользователя %s: " % comment.user,
            "mail/mail_article_comment.html",
            {
                "comment": comment,
                "parent_commit": comment.parent
            }
        )
