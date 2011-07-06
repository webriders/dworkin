# -*- coding: UTF-8 -*-

from techblog.logic.mail_service import MailService

def on_user_activate(request, user, **kwargs):
    MailService.send_mail_on_user_activate(request, user)


def on_article_comment(request, comment, **kwargs):
    MailService.send_mail_on_article_comment(comment)
