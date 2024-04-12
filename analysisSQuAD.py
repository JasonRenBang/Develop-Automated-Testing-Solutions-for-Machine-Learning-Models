import json
from openai import OpenAI
import getAnswers

def getQuestionsData(fileName):
    dataOriginal ={}
    with open("questions.json") as f:
        dataOriginal = json.load(f)

    dataParagraphs = []

    for item in dataOriginal['data']:
        dataParagraphs.append(item['paragraphs'])

    questions = []
    for item in dataParagraphs:
        for i in item:
            for question in i['qas']:
                questions.append(question['question'])

    questions = questions[:1000]
    print("Get Question done: ", len(questions))
    return questions



    # answersFromOrigianl = []
    # for item in dataParagraphs:
    #     for i in item:
    #         for answer in i['qas']:
    #             answerList = answer['answers']
    #             if len(answerList) == 0:
    #                 answerforQuestion = "There is no answer for this question."
    #             else:
    #                 answerforQuestion = answerList[0].get('text')
                    
    #             answersFromOrigianl.append(answerforQuestion)

    # answersFromOrigianl = answersFromOrigianl[:100]


    # answers = []

    # client = OpenAI()
    # for question in questions:
    #     completion = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "Give the question's answer."},
    #             {"role": "user", "content": question},
    #         ]
    #     )
    #     answers.append(completion.choices[0].message.content)
    # return questions, answers, 

def loadQuestionsAndAnswers(fileName):
    questions = getQuestionsData(fileName)
    answersOpenAI = getAnswers.getAnswersFromOpenAI(questions)
    answersGemini = getAnswers.getAnswersFromGemini(questions)

    return questions, answersOpenAI, answersGemini



dataOriginal ={}
datapackages = []
with open("dev-v1.1.json") as f:
    dataOriginal = json.load(f)
for item in dataOriginal['data']:

    for i in item['paragraphs']:
        datapackage = {}
        paragraph = i['context']
        datapackage['context'] = paragraph
        questionsList = []
        for question in i['qas']:
            q = question['question']
            questionsList.append(q)
        datapackage['questions'] = questionsList
        datapackages.append(datapackage)
print(len(datapackages))

