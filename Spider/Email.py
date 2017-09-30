import smtplib
from email.mime.text import MIMEText

mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "1562792894@qq.com"  # 用户名
mail_pass = "yxombnjhhahpghga"  # 口令

# msg = MIMEText("The body of the email is here")
# msg['Subject'] = "An Email Alert"
# msg['From'] = "1562792894@qq.com"
# msg['To'] = "1562792894@qq.com"

sender = '1562792894@qq.com'
receivers = ['1562792894@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = "1562792894@qq.com"
message['To'] = "1562792894@qq.com"
message['Subject'] = "Python邮件测试"

smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
# smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
smtpObj.login(mail_user, mail_pass)
smtpObj.sendmail(sender, receivers, message.as_string())
print("发送成功")
