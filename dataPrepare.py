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



# #method: need to encapsulate into a class
# def analyze_sentence(content):
#   listOfPos = []
#   listOfTags = []
#   listOfDeps = []
#   doc = nlp(content)
#   for token in doc:
#     listOfPos.append(token.pos_)
#     listOfTags.append(token.tag_)
#     listOfDeps.append(token.dep_)
#   return listOfPos, listOfTags, listOfDeps


# def generate_random_weekdays(content):
#   doc = nlp(content)
#   for token in doc:
#     if token.text.lower() in config.WEEKDAYS:
#       newDay = choice([d for d in config.WEEKDAYS if d != token.text.lower()])
#       newDay = newDay.capitalize()
#       # print("Replacing", token.text, "with", newDay)
#       content = content.replace(token.text, newDay)
#   return content

# def generate_random_date(content):
#   start_date = datetime(1990, 1, 1)
#   end_date = datetime(2030, 12, 31)
#   time_between_dates = end_date - start_date
#   days_between_dates = time_between_dates.days
#   random_number_of_days = randint(0, days_between_dates)
#   random_date = start_date + timedelta(days=random_number_of_days)
#   random_date = random_date.strftime("%d-%m-%Y")

#   doc = nlp(content)
#   for ent in doc.ents:
#     if ent.label_ == "DATE":
#       content = content.replace(ent.text, random_date)
#   return content
  
# def generate_random_numbers(content):
#   doc = nlp(content)
#   for ent in doc.ents:
#     if ent.label_ in ["CARDINAL", "PERCENT"]:
#       if "%" in ent.text: 
#           new_percent = f"{randint(1, 100)}%"
#           content = content.replace(ent.text, new_percent)
#       else: 
#           new_number = str(randint(1, 100))
#           content = content.replace(ent.text, new_number)
#   return content

# def generate_random_citiesAndCountries(content):
#   doc = nlp(content)
#   for ent in doc.ents:
#     if ent.label_ in ["GPE"]:
#       if ent.text in config.CITIES:
#         new_city = choice([c for c in config.CITIES if c != ent.text])
#         content = content.replace(ent.text, new_city)
#       elif ent.text in config.COUNTRIES:
#         new_country = choice([c for c in config.COUNTRIES if c != ent.text])
#         content = content.replace(ent.text, new_country)
#       elif ent.text in config.STATES:
#         new_state = choice([state for state in  config.STATES if state != ent.text])
#         content = content.replace(ent.text, new_state)

#   return content

# def generate_random_quantifiers(content):
#   matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
#   patterns = [nlp.make_doc(text) for text in config.QUANTIFIERS]
#   matcher.add("QUANTIFIERS", patterns)
#   doc = nlp(content)
#   matches = matcher(doc)
#   new_text = []
#   last_end = 0
#   for match_id, start, end in matches:
#     new_text.append(doc[last_end:start].text)
#     quantifiers_except_current = [q for q in config.QUANTIFIERS if q != doc[start:end].text.lower()]
#     new_quantifier = choice(quantifiers_except_current)
#     # print("Replacing", doc[start:end].text, "with", new_quantifier)
#     new_text.append(new_quantifier)
#     last_end = end
#   new_text.append(doc[last_end:].text)
#   new_text = " ".join(new_text)
#   return new_text

# def find_synonyms(word,pos):
#   antonyms = []
#   wn_pos = {'ADJ': wn.ADJ, 'ADV': wn.ADV, 'VERB': wn.VERB}.get(pos, None)
#   if wn_pos:
#     for syn in wn.synsets(word, pos=wn_pos):
#         for lemma in syn.lemmas():
#             if lemma.antonyms():
#                 antonyms.append(lemma.antonyms()[0].name())
#   return antonyms[0] if antonyms else None
# def generate_antonyms(content):
#   doc = nlp(content)
#   new_text = []
#   for token in doc:
#     antonym = None
#     if token.pos_ in ["ADJ", "ADV", "VERB"]:
#       antonym = find_synonyms(token.lemma_, token.pos_)
#     new_text.append(antonym if antonym else token.text)
#   new_text_str = " ".join(new_text)
#   return new_text_str

# def generate_NONE_NEGATIVE_words(content):
#   doc = nlp(content)
#   new_text = []
#   for token in doc:
#     if token.text.lower() not in config.NEGATIVE_WORDS and token.dep_ != "neg":
#         new_text.append(token.text_with_ws)
#   new_text_str = "".join(new_text).strip()
#   return new_text_str

# def get_subtree_indices(token):
#     return [t.i for t in token.subtree]
# def generate_word_delete(content):
#   doc = nlp(content)
#   to_delete = []
#   for token in doc:
#     if token.dep_ in ["amod", "nummod", "advmod", "nmod", "npadvmod", "relcl", "acl", "prep"]:
#         if random.random() < 0.5:  
#             subtree_indices = [t.i for t in token.subtree]
#             to_delete.extend(subtree_indices)
#   Token.set_extension("keep", default=True, force=True)
#   processed_text = " ".join([token.text_with_ws for i, token in enumerate(doc) if i not in to_delete]).rstrip()
#   return processed_text

# def generate_word_swap(content):

#   L1= nlp(content)
#   sentences = [sent.text for sent in L1.sents]
#   text = ""
#   client = OpenAI()
#   for sentence in sentences:
#     completion = client.chat.completions.create(
#       model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "Find the subject and predicate in the sentence, switch them positions, and then reconstruct them into a readable and understandable sentence"},
#             {"role": "user", "content": sentence},
#         ]
#     )
#     result = completion.choices[0].message.content
#     text += result 
#   return text

# def generate_check(content):
#   client = OpenAI()
#   completion = client.chat.completions.create(
#       model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "Check if the content is grammatically correct and make any necessary changes to ensure it is grammatically correct. And then reconstruct the content into a readable and understandable content."},
#             {"role": "user", "content": content},
#         ]
#     )
#   result = completion.choices[0].message.content
#   result = ' '.join(sentence.strip() for sentence in result.split('\n') if sentence.strip())
#   return result




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



