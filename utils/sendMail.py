import smtplib
import random

from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header


class MailSender:

    tmoji = ['(o°ω°o)', 'φ(>ω<*)', '∩( ·ω·)∩', 'ε = = (づ′▽`)づ ', '╮(￣▽￣)╭', '(づ●─●)づ']

    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"            # 设置服务器
    mail_user = "yejue@yjstudy1.com"     # 用户名（qq 可填@qq.com，或域名邮箱）
    mail_pass = "填你自己的"       # 口令

    sender = 'yejue@yjstudy1.com'       # 必须为当前用户名的可用邮箱（可以是你的域名邮箱或其他有权限邮箱）
    receivers = []                      # 接收邮件，可设置为你的QQ邮箱或者其他邮箱, 可设置多个

    def __init__(self, receivers, content):
        self.receivers.extend(receivers)
        self.content = content
        self.messages()

    def messages(self):
        self.message = MIMEText(self.content, 'plain', 'utf8')
        self.message['From'] = formataddr(["庸了个白", self.mail_user])
        self.message['To'] = Header('an', 'utf8')

        subject = '恭喜你找到验证码'
        self.message['Subject'] = Header(subject, 'utf-8')

    def senderFunc(self):
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, self.message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)
            print("Error: 无法发送邮件")


if __name__ == '__main__':
    sender = MailSender(["1145331931@qq.com"], "写点什么")
    sender.senderFunc()
