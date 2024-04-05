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
        if len(answersChatGPT)%10 == 0:
            print("Get Answers: ", len(answersChatGPT))
    print("Get Answers done: ", len(answersChatGPT))
    return answersChatGPT

def getAnswersFromGemini(questions):
    Api_Key = config.GOOGLE_API_KEY
    genai.configure(api_key=Api_Key)
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]
    answersGemini = []
    for question in questions:
        response = None
        max_attempts = 10
        attempts = 0
        

        while response is None and attempts < max_attempts:
          try:
            model = genai.GenerativeModel('gemini-pro',safety_settings=safety_settings )  
            # messages = [
            #   {'role':'user',
            #    'parts': ["Give the question's answer in a paragraph. and the question is: " + question]}
            # ]
            # response = model.generate_content(messages)
            # messages.append({'role':'model','parts':[response.text]})

            # messages.append({'role':'user','parts':[question]})

            # response = model.generate_content(messages)
            response = model.generate_content("Give the question's answer in a paragraph. and the question is: " + question)
          except Exception as e:
              print(f"Error for question {questions.index(question)}: {e}, Attempts: {attempts + 1}")
              attempts += 1
               
              continue
              
        

        answersGemini.append(response.text)
        print("Get Answers: ", len(answersGemini))
    print("Get Answers done: ", len(answersGemini))

    return answersGemini