import dataPrepare
import prototype2
import analysisSQuAD
import getAnswers
import celebritiesData
def main1paragraphDataPrepare():
  fileName = 'paragraphysData2.txt'
  topics, contents, paraphrases, transformations = dataPrepare.prepareData(fileName)

  for i in range(len(topics)):
    with open('dataOandPMAutomated2.txt', 'a',encoding='utf-8') as file:
        file.write('Topic: ' + topics[i] + '\n')
        file.write('  \n')
        file.write('Original paragraph  \n')
        file.write(contents[i] + '\n')
        file.write('  \n')
        file.write('Paraphrased paragraph  \n')
        file.write(paraphrases[i]+ '\n')
        file.write('  \n')
        file.write('Transformed paragraph  \n')
        file.write(transformations[i]+ '\n')
        file.write('  \n')


def main2paragraphResult():
  fileName = 'dataOandPMAutomated.txt'
  entities = prototype2.analyze_paragraphs(fileName)
  prototype2.get_results(entities)

def main3questionDataPrePare():
  fileName = 'questions.json'
  questions, answers, questionsP, answersP, questionsT, answersT = dataPrepare.create_ParaphraseAndTransformations_QA(fileName)

  for i in range(len(questions)):
    with open('dataOandPMAutomatedQA2.txt', 'a',encoding='utf-8') as file:
        file.write('Question: ' + str(i+1) + '\n')
        file.write('  \n')
        file.write('Original question  \n')
        file.write(questions[i] + '\n')
        file.write('  \n')
        file.write('Paraphrased question  \n')
        file.write(questionsP[i]+ '\n')
        file.write('  \n')
        file.write('Transformed question  \n')
        file.write(questionsT[i]+ '\n')
        file.write('  \n')
        file.write('Original question answer  \n')
        file.write(answers[i]+ '\n')
        file.write('  \n')
        file.write('Paraphrased question answer  \n')
        file.write(answersP[i]+ '\n')
        file.write('  \n')
        file.write('Transformed question answer  \n')
        file.write(answersT[i]+ '\n')
        file.write('  \n')

def main4questionResult():
  fileName = 'dataOandPMAutomatedQA2.txt'
  entities = prototype2.analyze_questions(fileName)
  prototype2.get_QAResult(entities)


def main5getQuestionsData():
  fileName = 'questions.json'
  questions, answersOpenAI, answersGemini = analysisSQuAD.loadQuestionsAndAnswers(fileName)


  for i in range(len(questions)):
    with open('dataOiginal2.txt', 'a',encoding='utf-8') as file:
        file.write('Question: ' + str(i+1) + '\n')
        file.write('  \n')
        file.write('Original question  \n')
        file.write(questions[i] + '\n')
        file.write('  \n')
        file.write('Get Answer from OpenAI  \n')
        file.write(answersOpenAI[i]+ '\n')
        file.write('  \n')
        file.write('Get Answer from Gemini  \n')
        file.write(answersGemini[i]+ '\n')
        file.write('  \n')


def main6getQuestionsAnalysis():
  fileName = 'dataOiginal2.txt'
  entities = prototype2.analyze_questions(fileName)
  print("Get start analysis")
  print(" ")
  prototype2.get_QAResult(entities)
  

def main7getCelebritiesData():
  fileName = 'compositional_celebrities.json'
  questions = celebritiesData.getCelebritiesData(fileName)
  answersGemini = getAnswers.getAnswersFromGemini(questions)
  answersOpenAI = getAnswers.getAnswersFromOpenAI(questions)
  for i in range(len(questions)):
    with open('celebritiesQuestionsData.txt', 'a',encoding='utf-8') as file:
        file.write('Question: ' + str(i+1) + '\n')
        file.write('  \n')
        file.write('Original question  \n')
        file.write(questions[i] + '\n')
        file.write('  \n')
        file.write('Get Answer from OpenAI  \n')
        file.write(answersOpenAI[i]+ '\n')
        file.write('  \n')
        file.write('Get Answer from Gemini  \n')
        file.write(answersGemini[i]+ '\n')
        file.write('  \n')


def main7CelebritiesAnalysis():
  fileName = 'celebritiesQuestionsData.txt'
  entities = prototype2.analyze_questions(fileName)
  print("Get start analysis")
  print(" ")
  prototype2.get_QAResult(entities)


def main8getQAPackageData():
  fileName = 'dev-v1.1.json'
  packages, realAnswers = analysisSQuAD.getQAData(fileName)

  questions, answersGemini, history = getAnswers.getAnswersFromGemini2(packages)
  print(len(questions))
  questions2, answersOpenAI, history2 = getAnswers.getAnswersFromOpenAI3(packages)

  for i in range(len(questions)):
    with open('dataOiginal5.txt', 'a',encoding='utf-8') as file:
        file.write('Question: ' + str(i+1) + '\n')
        file.write('  \n')
        file.write('Original question  \n')
        file.write(questions[i] + '\n')
        file.write('  \n')
        file.write('Get Answer from OpenAI  \n')
        file.write(answersOpenAI[i]+ '\n')
        file.write('  \n')
        file.write('Get Answer from Gemini  \n')
        file.write(answersGemini[i]+ '\n')
        file.write('  \n')
  for i in range(len(questions)):
    with open('QARealAnswers2.txt', 'a', encoding='utf-8') as file:
        file.write('Question: ' + str(i+1) + '\n')
        file.write('  \n')
        file.write('The question  \n')
        file.write(questions[i] + '\n')
        file.write('  \n')
        file.write('The Real Answer \n')
        file.write(realAnswers[i]+ '\n')
        file.write(' \n')
def main9getQAAnalysis():
  fileName = 'dataOiginal5.txt'
  entities = prototype2.analyze_questions(fileName)
  print("Get start analysis")
  print(" ")
  prototype2.get_QAResult(entities)
if __name__=="__main__":
  main9getQAAnalysis()
