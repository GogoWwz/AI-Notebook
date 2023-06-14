import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def send_email_action(receiver, content):
  if (not receiver): return
  # 邮件配置
  smtp_server = "smtp.163.com"
  smtp_port = 25
  sender_email = "sender_email"
  receiver_email = receiver
  password = 'password'

  # 构建邮件内容
  message = MIMEMultipart()
  message["From"] = Header('AI <%s>' % sender_email)
  message["To"] = receiver_email
  message["Subject"] = "我是您的AI助理，您有一封邮件请查看"

  body = content
  message.attach(MIMEText(body, "plain"))

  # 连接到邮件服务器并发送邮件
  with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

def send_email(receiver, content = ''):
  # 通讯录
  Contact = {
    "小美": "xx@example.com",
  }

  email_info = {
    "receiver": Contact[receiver],
    "content": content
  }

  return email_info
