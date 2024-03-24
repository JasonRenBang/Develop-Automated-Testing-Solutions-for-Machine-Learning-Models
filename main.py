import dataPrepare
import prototype2

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

if __name__=="__main__":
  main4questionResult()