import dataPrepare
import prototype2

def main1():
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


def main2():
  fileName = 'dataOandPMAutomated.txt'
  prototype2.analyze_paragraphs(fileName)

if __name__=="__main__":
  main1()