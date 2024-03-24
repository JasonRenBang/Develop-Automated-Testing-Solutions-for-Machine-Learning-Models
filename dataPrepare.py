from openai import OpenAI
import spacy
from sentence_transformers import SentenceTransformer, util
import config

import random
from random import choice
from random import randint
from datetime import datetime, timedelta
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token
import nltk
from nltk.corpus import wordnet as wn
import transformation
import analysisSQuAD




def create_ParaphraseAndTransformations_Content(fileName):

    topics = []
    contents = []

    with open(fileName, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith('Topic:'):
                topic = lines[i].split(':')[1].strip()
                i += 1
                content = ""
                while i < len(lines) and not lines[i].startswith('Topic:'):
                    content += lines[i].strip() + " "
                    i += 1
                topics.append(topic)
                contents.append(content.strip())


    print("Topics:", topics)
    # print("Contents:", contents)

    paraphrases = []

    for content in contents:
        client = OpenAI()
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you help me paraphrase this paragraph with the same number of sentences"},
                    {"role": "user", "content": content},
                ]
            )
        paraphrase = completion.choices[0].message.content
        paraphrases.append(paraphrase)
        print(content)
        print(" ")
        print("Paraphrase version: ",paraphrase)
        print(" ")

    transformations = [ ]
    # nltk.download('wordnet')
    # nlp = spacy.load("en_core_web_sm")
    for content in contents:
        content = transformation.generate_random_citiesAndCountries(content)
        content = transformation.generate_random_weekdays(content)
        content = transformation.generate_random_date(content)
        content = transformation.generate_random_numbers(content)
        content = transformation.generate_random_quantifiers(content)
        content = transformation.generate_antonyms(content)
        content = transformation.generate_NONE_NEGATIVE_words(content)
        content = transformation.generate_word_delete(content)
        content = transformation.generate_word_swap(content)
        content = transformation.generate_check(content)
        print("Transformed version: ",content)
        print(" ")
        transformations.append(content)
    return topics, contents, paraphrases, transformations



# for i in range(len(topics)):
#     with open('dataOandPMAutomated2.txt', 'a',encoding='utf-8') as file:
#         file.write('Topic: ' + topics[i] + '\n')
#         file.write('  \n')
#         file.write('Original paragraph  \n')
#         file.write(contents[i] + '\n')
#         file.write('  \n')
#         file.write('Paraphrased paragraph  \n')
#         file.write(paraphrases[i]+ '\n')
#         file.write('  \n')
#         file.write('Transformed paragraph  \n')
#         file.write(transformations[i]+ '\n')
#         file.write('  \n')



def create_ParaphraseAndTransformations_QA(fileName):
    questions, answers = analysisSQuAD.readQuestionsData(fileName)


    questionsP = []
    answersP = []

    for question in questions:
        client = OpenAI()
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Could you help me paraphrase this question"},
                    {"role": "user", "content": question},
                ]
            )
        questionP = completion.choices[0].message.content
        questionsP.append(questionP)
        print(question)
        print(" ")
        print("The question's answer: ",answers[questions.index(question)])
        print(" ")
        print("Paraphrase version: ",questionP)
        print(" ")

        completion2 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Answer the question."},
                    {"role": "user", "content": questionP},
                ]
            )
        answerP = completion2.choices[0].message.content
        answersP.append(answerP)
        
        print("The paraphrased question's answer: ",answerP)
        print(" ")

        

    questionsT = [ ]
    answersT = []
    # nltk.download('wordnet')
    # nlp = spacy.load("en_core_web_sm")
    for question in questions:
        questionT = transformation.generate_random_citiesAndCountries(question)
        questionT = transformation.generate_random_weekdays(questionT)
        questionT = transformation.generate_random_date(questionT)
        questionT = transformation.generate_random_numbers(questionT)
        questionT = transformation.generate_random_quantifiers(questionT)
        questionT = transformation.generate_antonyms(questionT)
        questionT = transformation.generate_NONE_NEGATIVE_words(questionT)
        questionT = transformation.generate_word_delete(questionT)
        questionT = transformation.generate_word_swap(questionT)
        questionT = transformation.generate_check(questionT)
        print("Transformed version: ",questionT)
        print(" ")
        questionsT.append(questionT)


        completion3 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Answer the question."},
                    {"role": "user", "content": questionT},
                ]
            )
        answerT = completion3.choices[0].message.content
        answersT.append(answerT)
        print("The transformed question's answer: ",answerT)
        print(" ")

    return questions, answers, questionsP, answersP, questionsT, answersT