from openai import OpenAI
import spacy
from sentence_transformers import SentenceTransformer, util
import config
import pandas as pd



# def is_meaningful_sentence(sentence):
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(sentence)
#     return any(token.dep_ == 'ROOT' for token in doc)



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
    answersOpenAI = []
    answersGemini = []

    with open(fileName, 'r', encoding='utf-8') as file:
        currentquestionIndex = ''
        currentQuestion = ''
        currentAnswerOpenAI = ''
        currentAnswerGemini = ''

        mode = 'QUESTION' #chase the current data mode: question, answerOpenAI, answerGemini
        for line in file:
            line = line.strip()
            if line.startswith('Question:'):
                if currentquestionIndex !='':
                    questionIndexs.append(currentquestionIndex)
                    questions.append(currentQuestion)
                    answersOpenAI.append(currentAnswerOpenAI)
                    answersGemini.append(currentAnswerGemini)

                    currentQuestion = ''
                    currentAnswerOpenAI = ''    
                    currentAnswerGemini = ''
                currentquestionIndex = line[len('Question: '):]
                mode = 'QUESTION'
            elif line=='Original question':
                mode = 'ORIGINALQUESTION'
            elif line=='Get Answer from OpenAI':
                mode = 'ANSWEROPENAI'
            elif line=='Get Answer from Gemini':
                mode = 'ANSWERGEMINI'
            else:
                if mode=='ORIGINALQUESTION':
                    currentQuestion += line
                elif mode=='ANSWEROPENAI':
                    currentAnswerOpenAI += line
                elif mode=='ANSWERGEMINI':
                    currentAnswerGemini += line

        if currentQuestion !='':
            questionIndexs.append(currentquestionIndex)
            questions.append(currentQuestion)
            answersOpenAI.append(currentAnswerOpenAI)   
            answersGemini.append(currentAnswerGemini)

    
    entities = []   
    for i in range(len(questionIndexs)):
        questionIndex = questionIndexs[i]
        question = questions[i]
        answerOpenAI = answersOpenAI[i]
        answerGemini = answersGemini[i]
        entities.append((questionIndex, question, answerOpenAI, answerGemini))
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
        [('OpenAI vs Gemini\'', 'contradiction'), ('OpenAI vs Gemini', 'not contradiction')],
        names=['Question', ' ']
    )
    data = []
    numOfSentences = config.NUMBER_OF_SUMMARY_SENTENCES
    wordLimit = config.WORD_LIMIT_FOR_EACH_SENTENCE
    questionIndexs = []
    
    for entity in entities:
        questionIndex = entity[0]
        questionIndexs.append(questionIndex)
        question = entity[1]
        answerOpenAI = entity[2]
        answerGemini = entity[3]

        with open('QA_outcomes4.txt', 'a',encoding='utf-8') as file:
            file.write('--------------------------------------------------------------\n')
            file.write('Question Index: ' + questionIndex + '\n')
            file.write('  \n')
            file.write('Original question  \n')
            file.write(question + '\n')
            file.write('  \n')
            file.write('Get Answer from OpenAI  \n')
            file.write(answerOpenAI + '\n')
            file.write('  \n')
            file.write('Get Answer from Gemini  \n')
            file.write(answerGemini + '\n')
            file.write('  \n')

        print("Question Index: ", questionIndex)
        print("  ")
        print("Original question  \n")
        print(question)
        print("  ")
        print("Get Answer from OpenAI  \n")
        print(answerOpenAI)
        print("  ")
        print("Get Answer from Gemini  \n")
        print(answerGemini)
        print("  ")

        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Could you help me summarize this paragraph in " + str(numOfSentences)+ " short sentences within the word limit of "+ str(wordLimit)+ " words"},
                {"role": "user", "content": answerOpenAI},
            ]
        )
        sum1 = completion.choices[0].message.content

        completion2 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Could you help me summarize this paragraph in " + str(numOfSentences)+ " short sentences within the word limit of "+ str(wordLimit)+ " words"},
                {"role": "user", "content": answerGemini},
            ]
        )
        sum2 = completion2.choices[0].message.content
        with open('QA_outcomes4.txt', 'a',encoding='utf-8') as file:
            file.write('Their summary produced by ChatGPT are:\n')
            file.write('Summary1 for OpenAI answer:  \n')
            file.write(sum1 + '\n')
            file.write('  \n')
            file.write('Summary2 for Gemini answer:  \n')
            file.write(sum2 + '\n')
            file.write('  \n')
        print("Their summary produced by ChatGPT are:\n")
        print("Summary1 for OpenAI answer:  \n")
        print(sum1)
        print("  ")
        print("Summary2 for Gemini answer:  \n")
        print(sum2)
        print("  ")

        min_length = config.MIN_SENTENCE_LENGTH
        nlp = spacy.load("en_core_web_sm")
        model = SentenceTransformer('all-MiniLM-L6-v2')

        L1= nlp(sum1)
        
        sentences1 = [sent.text for sent in L1.sents]
        print(len(sentences1))

        sentences1 = [sent for sent in sentences1 if len(sent.split()) > min_length]
 #       sentences1 = [sent for sent in sentences1 if is_meaningful_sentence(sent)]
        print("sentences1", sentences1)
        print(len(sentences1))


        L2= nlp(sum2)
        sentences2 = [sent.text for sent in L2.sents]
        sentences2 = [sent for sent in sentences2 if len(sent.split()) > min_length]
 #       sentences2 = [sent for sent in sentences2 if is_meaningful_sentence(sent)]
        print("sentences2", sentences2)
        print(len(sentences2))

        embeddings1 = model.encode(sentences1, convert_to_tensor=True)
        embeddings2 = model.encode(sentences2, convert_to_tensor=True)

        cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
        matched_sentences_and_scores = []
        for i in range(len(sentences1)):
            best_match_idx  = cosine_scores[i].argmax().item()
            best_score = cosine_scores[i][best_match_idx].item()
            matched_pair = (sentences1[i], sentences2[best_match_idx], best_score)
            matched_sentences_and_scores.append(matched_pair)
        print("results for OpenAI and Gemini", matched_sentences_and_scores)
        print(" ")
        print("After pairing, we have identified the following pairs\n")
        print("  ")

        contradiction = 0
        notcontradiction = 0

        resultspp = []
        for pair in matched_sentences_and_scores:
            sentence1 = pair[0]
            sentence2 = pair[1]
            completion3 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you tell me if these two sentences are contradicting each other. If they are contradicting, please say True first, otherwise say False. And then tell me the reason."},
                    {"role": "user", "content": sentence1},
                    {"role": "user", "content": sentence2}
                ]
            )
            result = completion3.choices[0].message.content
            resultspp.append((sentence1,sentence2,result))

            if result.startswith('True'):
                contradiction  = contradiction+ 1
            else:
                notcontradiction = notcontradiction+ 1

            print(sentence1)
            print(" and ")
            print(sentence2)
            print("  : ")
            print(result)
            print("  ")
        data.append([contradiction, notcontradiction])

        with open('QA_outcomes4.txt', 'a',encoding='utf-8') as file:
            file.write('The results of the contradiction detection are:\n')
            file.write('For OpenAI and Gemini\n')
            for i in range(len(resultspp)):
                file.write('Pair ' + str(i+1) + ':')
                file.write('  \n')
                file.write(resultspp[i][0] + '\n')
                file.write("  \n")
                file.write(resultspp[i][1] + '\n')
                file.write('  \n')
                file.write('Result: ' + resultspp[i][2] + '\n')
                file.write('  \n')
            file.write('  \n')
    df = pd.DataFrame(data, index=questionIndexs, columns=multi_columns)
    print(df)
    print("  ")
    df.to_csv('QA_outcomes4.csv')
    print("Done")