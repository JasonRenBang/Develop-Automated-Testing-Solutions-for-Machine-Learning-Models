import json
from openai import OpenAI


dataOriginal ={}
with open('questions.json') as f:
    dataOriginal = json.load(f)

# print(len(dataOriginal['data'][0]['paragraphs'][0]['qas']))

# print(len(dataOriginal['data']))

dataParagraphs = []

for item in dataOriginal['data']:
    dataParagraphs.append(item['paragraphs'])

questions = []
for item in dataParagraphs:
    for i in item:
        for question in i['qas']:
            questions.append(question['question'])

questions = questions[:100]

answers = []

client = OpenAI()
for question in questions:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Give the question's answer."},
            {"role": "user", "content": question},
        ]
    )
    answers.append(completion.choices[0].message.content)

print(answers[:10])
