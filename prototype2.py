from openai import OpenAI
import spacy
from sentence_transformers import SentenceTransformer, util
import config
import pandas as pd


def analyze_paragraphs(fileName):

    topics = []
    originals = []
    paraphrases = []
    #manualTransformations = []
    transformers = []

    with open(fileName, 'r', encoding='utf-8') as file:
        currentTopic = ''
        currentOriginal = ''
        currentParaphrase = ''
        #currentManualTransformation = ''
        currentTransformation = ''
        mode = 'TOPIC' #chase the current data mode: topic, original, paraphrase, manualTransformation
        for line in file:
            line = line.strip()
            if line.startswith('Topic:'):
                if currentTopic !='':
                    topics.append(currentTopic)
                    originals.append(currentOriginal)
                    paraphrases.append(currentParaphrase)
    #                manualTransformations.append(currentManualTransformation)
                    transformers.append(currentTransformation)

                    currentOriginal = ''
                    currentParaphrase = ''
    #                currentManualTransformation = ''
                    currentTransformation = ''
                currentTopic = line[len('Topic: '):]
                mode = 'TOPIC'
            elif line=='Original paragraph':
                mode = 'ORIGINALPARAGRAPH'
            elif line=='Paraphrased paragraph':
                mode = 'PARAPHRASEDPARAGRAPH'
            # elif line=='Manual transformation':
            #     mode = 'MANUALTRANSFORMATION'
            elif line=='Transformed paragraph':
                mode = 'TRANSFORMATION'
            else:
                if mode=='ORIGINALPARAGRAPH':
                    currentOriginal += line
                elif mode=='PARAPHRASEDPARAGRAPH':
                    currentParaphrase += line
                # elif mode=='MANUALTRANSFORMATION':
                #     currentManualTransformation += line
                elif mode=='TRANSFORMATION':
                    currentTransformation += line
        if currentTopic !='':
            topics.append(currentTopic)
            originals.append(currentOriginal.strip())
            paraphrases.append(currentParaphrase.strip())
    #        manualTransformations.append(currentManualTransformation.strip())
            transformers.append(currentTransformation.strip())



    entities = []
    for i in range(len(topics)):
        topic = topics[i]
        content1 = originals[i]
        content2 = paraphrases[i]
        # content3 = manualTransformations[i]
        content3 = transformers[i]
        entities.append((topic, content1, content2, content3))

    return entities


def analyze_questions(fileName):
    questionIndexs = []
    questions = []
    answers = []
    questionsP = []
    answersP = []
    questionsT = []
    answersT = []

    with open(fileName, 'r', encoding='utf-8') as file:
        currentquestionIndex = ''
        currentQuestion = ''
        currentAnswer = ''
        currentQuestionP = ''
        currentAnswerP = ''
        currentQuestionT = ''
        currentAnswerT = ''
        mode = 'QUESTION' #chase the current data mode: question, answer, questionP, answerP, questionT, answerT
        for line in file:
            line = line.strip()
            if line.startswith('Question:'):
                if currentquestionIndex !='':
                    questionIndexs.append(currentquestionIndex)
                    questions.append(currentQuestion)
                    answers.append(currentAnswer)
                    questionsP.append(currentQuestionP)
                    answersP.append(currentAnswerP)
                    questionsT.append(currentQuestionT)
                    answersT.append(currentAnswerT)

                    currentQuestion = ''
                    currentAnswer = ''
                    currentQuestionP = ''
                    currentAnswerP = ''
                    currentQuestionT = ''
                    currentAnswerT = ''
                currentquestionIndex = line[len('Question: '):]
                mode = 'QUESTION'
            elif line=='Original question':
                mode = 'ORIGINALQUESTION'
            elif line=='Paraphrased question':
                mode = 'PARAPHRASEDQUESTION'
            elif line=='Transformed question':
                mode = 'TRANSFORMEDQUESTION'
            elif line=='Original question answer':
                mode = 'ORIGINALANSWER'
            elif line=='Paraphrased question answer':
                mode = 'PARAPHRASEDANSWER'
            elif line=='Transformed question answer':
                mode = 'TRANSFORMEDANSWER'
            else:
                if mode=='ORIGINALQUESTION':
                    currentQuestion += line
                elif mode=='PARAPHRASEDQUESTION':
                    currentQuestionP += line
                elif mode=='TRANSFORMEDQUESTION':
                    currentQuestionT += line
                elif mode=='ORIGINALANSWER':
                    currentAnswer += line
                elif mode=='PARAPHRASEDANSWER':
                    currentAnswerP += line
                elif mode=='TRANSFORMEDANSWER':
                    currentAnswerT += line
        if currentQuestion !='':
            questionIndexs.append(currentquestionIndex)
            questions.append(currentQuestion)
            answers.append(currentAnswer)
            questionsP.append(currentQuestionP)
            answersP.append(currentAnswerP)
            questionsT.append(currentQuestionT)
            answersT.append(currentAnswerT)
    
    entities = []   
    for i in range(len(questionIndexs)):
        questionIndex = questionIndexs[i]
        question = questions[i]
        answer = answers[i]
        questionP = questionsP[i]
        answerP = answersP[i]
        questionT = questionsT[i]
        answerT = answersT[i]
        entities.append((questionIndex, question, answer, questionP, answerP, questionT, answerT))
    return entities

def get_results(entities):
    multi_columns = pd.MultiIndex.from_tuples(
        [('PP\'', 'contradiction'), ('PP\'', 'not contradiction'), ('PP\'\'', 'contradiction'), ('PP\'\'', 'not conradiction')],
        names=['Topic', ' ']
    )
    data = []
    numOfSentences = config.NUMBER_OF_SUMMARY_SENTENCES
    wordLimit = config.WORD_LIMIT_FOR_EACH_SENTENCE
    topics = []
    
    for entity in entities:
        topic = entity[0]
        topics.append(topic)
        original = entity[1]
        paraphrase = entity[2]
    #    manualTransformation = entity[3]
        transformers = entity[3]

        with open('automated_outcomes_version.txt', 'a',encoding='utf-8') as file:
            file.write('--------------------------------------------------------------\n')
            file.write('Topic: ' + topic + '\n')
            file.write('  \n')
            file.write('Original paragraph  \n')
            file.write(original + '\n')
            file.write('  \n')
            file.write('Paraphrased paragraph  \n')
            file.write(paraphrase + '\n')
            file.write('  \n')
            # file.write('Manual transformation  \n')
            # file.write(manualTransformation + '\n')
            file.write('Transformation Paragraph  \n')
            file.write(transformers + '\n')
            file.write('  \n')
        
        print("Topic: ", topic)
        print("  ")
        print("Original paragraph  \n")
        print(original)
        print("  ")
        print("Paraphrased paragraph  \n")
        print(paraphrase)
        print("  ")
        # print("Manual transformation  \n")  
        # print(manualTransformation)
        print("Transformation Paragraph  \n")
        print(transformers)
        print("  ")


        client = OpenAI()
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you help me summarize this paragraph in " + str(numOfSentences)+ " short sentences within the word limit of "+ str(wordLimit)},
                    {"role": "user", "content": original},
                ]
            )
        sum1 = completion.choices[0].message.content

        completion2 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you help me summarize this paragraph in " + str(numOfSentences)+ " short sentences within the word limit of "+ str(wordLimit)},
                    {"role": "user", "content": paraphrase},
                ]
            )
        sum2 = completion2.choices[0].message.content

        completion3 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you help me summarize this paragraph in " + str(numOfSentences)+ " short sentences within the word limit of "+ str(wordLimit)},
                    # {"role": "user", "content": manualTransformation},
                    {"role": "user", "content": transformers},
                ]
            )
        sum3 = completion3.choices[0].message.content

        with open('automated_outcomes_version.txt', 'a',encoding='utf-8') as file:
            file.write('Their summary produced by ChatGPT are:\n')
            file.write('Summary1 for original content:  \n')
            file.write(sum1 + '\n')
            file.write('  \n')
            file.write('Summary2 for paraphrase content:  \n')
            file.write(sum2 + '\n')
            file.write('  \n')
            # file.write('Summary3 for manual transformation:  \n')
            # file.write(sum3 + '\n')
            file.write('Summary3 for transformation:  \n')
            file.write(sum3 + '\n')
            file.write('  \n')

        print("Their summary produced by ChatGPT are:\n")
        print("Summary1 for original content:  \n")
        print(sum1)
        print("  ")
        print("Summary2 for paraphrase content:  \n")
        print(sum2)
        print("  ")
        # print("Summary3 for manual transformation:  \n")
        # print(sum3)
        print("Summary3 for transformation:  \n")
        print(sum3)
        print("  ")

        nlp = spacy.load("en_core_web_sm")
        model = SentenceTransformer('all-MiniLM-L6-v2')

        L1= nlp(sum1)
        sentences1 = [sent.text for sent in L1.sents]

        L2= nlp(sum2)
        sentences2 = [sent.text for sent in L2.sents]

        L3= nlp(sum3)
        sentences3 = [sent.text for sent in L3.sents]

        embeddings1 = model.encode(sentences1, convert_to_tensor=True)
        embeddings2 = model.encode(sentences2, convert_to_tensor=True)
        embeddings3 = model.encode(sentences3, convert_to_tensor=True)


        cosine_scorespp = util.pytorch_cos_sim(embeddings1, embeddings2)
        matched_sentences_and_scores_pp = []
        for i in range(len(sentences1)):
            best_match_idx  = cosine_scorespp[i].argmax().item()
            best_score = cosine_scorespp[i][best_match_idx].item()
            matched_pair = (sentences1[i], sentences2[best_match_idx], best_score)
            matched_sentences_and_scores_pp.append(matched_pair)
        print("results for pp", matched_sentences_and_scores_pp)

        cosine_scoresppp = util.pytorch_cos_sim(embeddings1, embeddings3)
        matched_sentences_and_scores_ppp = []
        for i in range(len(sentences1)):
            best_match_idx  = cosine_scoresppp[i].argmax().item()
            best_score = cosine_scoresppp[i][best_match_idx].item()
            matched_pair = (sentences1[i], sentences3[best_match_idx], best_score)
            matched_sentences_and_scores_ppp.append(matched_pair)
        print("results for pppirme", matched_sentences_and_scores_ppp)

        print("After pairing, we have identified the following pairs\n")
        print("  ")
        print("For original and paraphrase\n")
        print("  ")
        ppcontradiction = 0
        ppnotcontradiction = 0
        pppcontradiction = 0
        pppnotcontradiction = 0
        resultspp = []
        for pair in matched_sentences_and_scores_pp:
            sentence1 = pair[0]
            sentence2 = pair[1]
            completion4 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you tell me if these two sentences are contradicting each other. If they are contradicting, please say True first, otherwise say False. And then tell me the reason."},
                    {"role": "user", "content": sentence1},
                    {"role": "user", "content": sentence2}
                ]
            )
            result = completion4.choices[0].message.content
            resultspp.append((sentence1,sentence2,result))

            if result.startswith('True'):
                ppcontradiction  = ppcontradiction+ 1
            else:
                ppnotcontradiction = ppnotcontradiction+ 1

            print(sentence1)
            print(" and ")
            print(sentence2)
            print("  : ")
            print(result)
            print("  ")
            
        # print("For original and manual transformation\n")
        print("For original and transformation\n")
        print("  ")
        resultsppp = []
        for pair in matched_sentences_and_scores_ppp:
            sentence1 = pair[0]
            sentence2 = pair[1]
            completion5 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you tell me if these two sentences are contradicting each other. If they are contradicting, please say True first, otherwise say False. And then tell me the reason."},
                    {"role": "user", "content": sentence1},
                    {"role": "user", "content": sentence2}
                ]
            )
            result = completion5.choices[0].message.content
            resultsppp.append((sentence1,sentence2,result))
            if result.startswith('True'):
                pppcontradiction = pppcontradiction+1
            else:
                pppnotcontradiction =pppnotcontradiction+ 1
                
            print(sentence1)
            print(" and ")
            print(sentence2)
            print("  : ")
            print(result)
            print("  ")
        data.append([ppcontradiction, ppnotcontradiction, pppcontradiction, pppnotcontradiction])

        with open('automated_outcomes_version.txt', 'a',encoding='utf-8') as file:
            file.write('The results of the contradiction detection are:\n')
            file.write('For original and paraphrase\n')
            for i in range(len(resultspp)):
                file.write('Pair ' + str(i+1) + ':')
                file.write('  \n')
                file.write(resultspp[i][0] + '\n')
                file.write("  \n")
                file.write(resultspp[i][1] + '\n')
                file.write('  \n')
                file.write('Result: ' + resultspp[i][2] + '\n')
                file.write('  \n')
            # file.write('For original and manual transformation\n')
            file.write('For original and transformation\n')
            for i in range(len(resultsppp)):
                file.write('Pair ' + str(i+1) + ':')
                file.write('  \n')
                file.write(resultsppp[i][0] + '\n')
                file.write("  \n")
                file.write(resultsppp[i][1] + '\n')
                file.write('  \n')
                file.write('Result: ' + resultsppp[i][2] + '\n')
                file.write('  \n')
            file.write('  \n')

    df = pd.DataFrame(data, index=topics, columns=multi_columns)
    print(df)
    print("  ")
    # with open('outcomes_version3.txt', 'a',encoding='utf-8') as file:
    #     file.write(df.to_string())

    df.to_csv('automated_outcomes_version.csv')



    print("Done")



def get_QAResult(entities):
    multi_columns = pd.MultiIndex.from_tuples(
        [('PP\'', 'contradiction'), ('PP\'', 'not contradiction'), ('PP\'\'', 'contradiction'), ('PP\'\'', 'not conradiction')],
        names=['Question', ' ']
    )
    data = []
    # numOfSentences = config.NUMBER_OF_SUMMARY_SENTENCES
    # wordLimit = config.WORD_LIMIT_FOR_EACH_SENTENCE
    questionIndexs = []
    
    for entity in entities:
        questionIndex = entity[0]
        questionIndexs.append(questionIndex)
        question = entity[1]
        answer = entity[2]
        questionP = entity[3]
        answerP = entity[4]
        questionT = entity[5]
        answerT = entity[6]

        with open('automated_outcomes_versionQA.txt', 'a',encoding='utf-8') as file:
            file.write('--------------------------------------------------------------\n')
            file.write('Question Index: ' + questionIndex + '\n')
            file.write('  \n')
            file.write('Original question  \n')
            file.write(question + '\n')
            file.write('  \n')
            file.write('Paraphrased question  \n')
            file.write(questionP + '\n')
            file.write('  \n')
            file.write('Transformed question  \n')
            file.write(questionT + '\n')
            file.write('  \n')
            file.write('Original question answer  \n')
            file.write(answer + '\n')
            file.write('  \n')
            file.write('Paraphrased question answer  \n')
            file.write(answerP + '\n')
            file.write('  \n')
            file.write('Transformed question answer  \n')
            file.write(answerT + '\n')
            file.write('  \n')

        print("Question Index: ", questionIndex)
        print("  ")
        print("Original question  \n")
        print(question)
        print("  ")
        print("Paraphrased question  \n")
        print(questionP)
        print("  ")
        print("Transformed question  \n")
        print(questionT)
        print("  ")
        print("Original question answer  \n")
        print(answer)
        print("  ")
        print("Paraphrased question answer  \n")
        print(answerP)
        print(" ")
        print("Transformed question answer  \n")
        print(answerT)
        print("  ")

        client = OpenAI()
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you help me summarize it in one sentence with 60 word limit"},
                    {"role": "user", "content": answer},
                ]
            )
        sum1 = completion.choices[0].message.content

        completion2 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you help me summarize it in one sentence with 60 word limit"},
                    {"role": "user", "content": answerP},
                ]
            )
        sum2 = completion2.choices[0].message.content
        
        completion3 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you help me summarize it in one sentence with 60 word limit"},
                    {"role": "user", "content": answerT},
                ]
            )
        sum3 = completion3.choices[0].message.content

        with open('automated_outcomes_versionQA.txt', 'a',encoding='utf-8') as file:
            file.write('Their summary produced by ChatGPT are:\n')
            file.write('Summary1 for original content:  \n')
            file.write(sum1 + '\n')
            file.write('  \n')
            file.write('Summary2 for paraphrase content:  \n')
            file.write(sum2 + '\n')
            file.write('  \n')
            file.write('Summary3 for transformation:  \n')
            file.write(sum3 + '\n')
            file.write('  \n')
        
        print("Their summary produced by ChatGPT are:\n")
        print("Summary1 for original content:  \n")
        print(sum1)
        print("  ")
        print("Summary2 for paraphrase content:  \n")
        print(sum2)
        print("  ")
        print("Summary3 for transformation:  \n")
        print(sum3)
        print("  ")

        ppcontradiction = 0
        ppnotcontradiction = 0
        pppcontradiction = 0
        pppnotcontradiction = 0

        completion4 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Could you tell me if these two answers are contradicting each other. If they are contradicting, please say True first, otherwise say False. And then tell me the reason."},
                {"role": "user", "content": answer},
                {"role": "user", "content": answerP}
            ]
        )
        result = completion4.choices[0].message.content
        if result.startswith('True'):
            ppcontradiction = ppcontradiction + 1
        else:
            ppnotcontradiction = ppnotcontradiction + 1
        
        with open('automated_outcomes_versionQA.txt', 'a',encoding='utf-8') as file:
            file.write('The results of the contradiction detection are:\n')
            file.write('For original and paraphrase\n')
            file.write('Result: ' + result + '\n')
            file.write('  \n')
        print('The results of the contradiction detection are:\n')
        print("For the answer of original question and paraphrase question: \n")
        print("  ")
        print(result)
        print("  ")

        completion5 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Could you tell me if these two answers are contradicting each other. If they are contradicting, please say True first, otherwise say False. And then tell me the reason."},
                {"role": "user", "content": answer},
                {"role": "user", "content": answerT}
            ]
        )
        result = completion5.choices[0].message.content
        if result.startswith('True'):
            pppcontradiction = pppcontradiction + 1
        else:
            pppnotcontradiction = pppnotcontradiction + 1
        with open('automated_outcomes_versionQA.txt', 'a',encoding='utf-8') as file:
            file.write('For original and transformation\n')
            file.write('Result: ' + result + '\n')
            file.write('  \n')
        print("For the answer of original question and paraphrase question: \n")
        print("  ")
        print(result)
        print("  ")
        data.append([ppcontradiction, ppnotcontradiction, pppcontradiction, pppnotcontradiction])


    df = pd.DataFrame(data, index=questionIndexs, columns=multi_columns)
    print(df)
    print("  ")
    # with open('outcomes_version3.txt', 'a',encoding='utf-8') as file:
    #     file.write(df.to_string())

    df.to_csv('QAautomated_outcomes_version.csv')

    print("Done")





        






      







