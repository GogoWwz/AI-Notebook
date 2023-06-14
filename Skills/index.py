import json
from enum import Enum
import openai
openai.api_key = 'xxx'

from EmailSkill import send_email, send_email_action

class SkillFunctions(Enum):
  SendEmail = 'send_email'

def run_conversation():
  MODEL = "gpt-3.5-turbo-0613"
  response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
      {"role": "user", "content": "给小美发个邮件，告诉她我晚饭不回家吃了"},
    ],
    temperature=0,
    functions=[
      {
        "name": SkillFunctions.SendEmail.value,
        "description": "send email assistant",
        "parameters": {
          "type": "object",
          "properties": {
            "receiver": {
              "type": "string",
              "description": "email receiver",
            },
            "content": {"type": "string", "description": "email content"},
          },
          "required": ["receiver", "content"],
        },
      }
    ],
    function_call="auto",
  )

  message = response["choices"][0]["message"]
  print(message)

  if(message.get("function_call")):
    function_name = message["function_call"]["name"]
    arguments = json.loads(message["function_call"]["arguments"])

    if (function_name == SkillFunctions.SendEmail.value):
      email_info = send_email(
        receiver=arguments.get('receiver'),
        content=arguments.get('content')
      )
      print(email_info)
      send_email_action(**email_info)
      print('邮件已发送')

run_conversation()