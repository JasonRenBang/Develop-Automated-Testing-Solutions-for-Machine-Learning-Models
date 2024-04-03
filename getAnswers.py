from openai import OpenAI
import google.generativeai as genai
import config

def getAnswersFromOpenAI(questions):
    answersChatGPT = []
    client = OpenAI()
    for question in questions:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Give the question's answer in a paragraph."},
                {"role": "user", "content": question},
            ]
        )
        answersChatGPT.append(completion.choices[0].message.content)
    return answersChatGPT

def getAnswersFromGemini(questions):
    Api_Key = config.GOOGLE_API_KEY
    genai.configure(api_key=Api_Key)
    answersGemini = []
    for question in questions:
        model = genai.GenerativeModel('gemini-pro')
        messages = [
            {'role':'user',
            'parts': [question]}
        ]
        response = model.generate_content(messages)

        messages.append({'role':'model',
                        'parts':[response.text]})

        messages.append({'role':'user',
                        'parts':["Give the question's answer in a paragraph."]})

        response = model.generate_content(messages, safety_settings={'HARASSMENT':'block_none'})
        answersGemini.append(response.text)


    return answersGemini