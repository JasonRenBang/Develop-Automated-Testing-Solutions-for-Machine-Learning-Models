import google.generativeai as genai
import config



Api_Key = config.GOOGLE_API_KEY
genai.configure(api_key=Api_Key)

model = genai.GenerativeModel('gemini-pro')
# messages = [{"role": "user", "parts": ["Give the question's answer in a sentence."]}]
# messages.append({"role": "model", "parts": ["When did Beyonce start becoming popular?"]})
# response = model.generate_content(messages, safety_settings={'HARASSMENT':'block_none'})




messages = [
    {'role':'user',
     'parts': ["When did Beyonce start becoming popular?"]}
]
response = model.generate_content(messages)
# print(response.text)
messages.append({'role':'model',
                 'parts':[response.text]})

messages.append({'role':'user',
                 'parts':["Give the question's answer in a sentence."]})

response = model.generate_content(messages, safety_settings={'HARASSMENT':'block_none'})
print(response.text)
