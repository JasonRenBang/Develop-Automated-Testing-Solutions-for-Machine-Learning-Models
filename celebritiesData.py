import json
import config

def getCelebritiesData(fileName):
  setQuestionNumber = config.QUESTION_NUMBER
  questions = []
  with open(fileName) as f:
      dataOriginal = json.load(f)
  for item in dataOriginal['data']:
      question = item['Question']
      questions.append(question)
  questions = questions[:setQuestionNumber]
  return questions


