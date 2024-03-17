import spacy
import config
import random
from random import choice
from random import randint
from datetime import datetime, timedelta
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token
import nltk
from nltk.corpus import wordnet as wn
from openai import OpenAI


def analyze_sentence(content):
  listOfPos = []
  listOfTags = []
  listOfDeps = []
  doc = nlp(content)
  for token in doc:
    listOfPos.append(token.pos_)
    listOfTags.append(token.tag_)
    listOfDeps.append(token.dep_)
  return listOfPos, listOfTags, listOfDeps


def generate_random_weekdays(content):
  doc = nlp(content)
  for token in doc:
    if token.text.lower() in config.WEEKDAYS:
      newDay = choice([d for d in config.WEEKDAYS if d != token.text.lower()])
      newDay = newDay.capitalize()
      # print("Replacing", token.text, "with", newDay)
      content = content.replace(token.text, newDay)
  return content

def generate_random_date(content):
  start_date = datetime(1990, 1, 1)
  end_date = datetime(2030, 12, 31)
  time_between_dates = end_date - start_date
  days_between_dates = time_between_dates.days
  random_number_of_days = randint(0, days_between_dates)
  random_date = start_date + timedelta(days=random_number_of_days)
  random_date = random_date.strftime("%d-%m-%Y")

  doc = nlp(content)
  for ent in doc.ents:
    if ent.label_ == "DATE":
      content = content.replace(ent.text, random_date)
  return content
  
def generate_random_numbers(content):
  doc = nlp(content)
  for ent in doc.ents:
    if ent.label_ in ["CARDINAL", "PERCENT"]:
      if "%" in ent.text: 
          new_percent = f"{randint(1, 100)}%"
          content = content.replace(ent.text, new_percent)
      else: 
          new_number = str(randint(1, 100))
          content = content.replace(ent.text, new_number)
  return content

def generate_random_citiesAndCountries(content):
  doc = nlp(content)
  for ent in doc.ents:
    if ent.label_ in ["GPE"]:
      if ent.text in config.CITIES:
        new_city = choice([c for c in config.CITIES if c != ent.text])
        content = content.replace(ent.text, new_city)
      elif ent.text in config.COUNTRIES:
        new_country = choice([c for c in config.COUNTRIES if c != ent.text])
        content = content.replace(ent.text, new_country)
      elif ent.text in config.STATES:
        new_state = choice([state for state in  config.STATES if state != ent.text])
        content = content.replace(ent.text, new_state)

  return content

def generate_random_quantifiers(content):
  matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
  patterns = [nlp.make_doc(text) for text in config.QUANTIFIERS]
  matcher.add("QUANTIFIERS", patterns)
  doc = nlp(content)
  matches = matcher(doc)
  new_text = []
  last_end = 0
  for match_id, start, end in matches:
    new_text.append(doc[last_end:start].text)
    quantifiers_except_current = [q for q in config.QUANTIFIERS if q != doc[start:end].text.lower()]
    new_quantifier = choice(quantifiers_except_current)
    # print("Replacing", doc[start:end].text, "with", new_quantifier)
    new_text.append(new_quantifier)
    last_end = end
  new_text.append(doc[last_end:].text)
  new_text = " ".join(new_text)
  return new_text

def find_synonyms(word,pos):
  antonyms = []
  wn_pos = {'ADJ': wn.ADJ, 'ADV': wn.ADV, 'VERB': wn.VERB}.get(pos, None)
  if wn_pos:
    for syn in wn.synsets(word, pos=wn_pos):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())
  return antonyms[0] if antonyms else None
def generate_antonyms(content):
  doc = nlp(content)
  new_text = []
  for token in doc:
    antonym = None
    if token.pos_ in ["ADJ", "ADV", "VERB"]:
      antonym = find_synonyms(token.lemma_, token.pos_)
    new_text.append(antonym if antonym else token.text)
  new_text_str = " ".join(new_text)
  return new_text_str

def generate_NONE_NEGATIVE_words(content):
  doc = nlp(content)
  new_text = []
  for token in doc:
    if token.text.lower() not in config.NEGATIVE_WORDS and token.dep_ != "neg":
        new_text.append(token.text_with_ws)
  new_text_str = "".join(new_text).strip()
  return new_text_str

def get_subtree_indices(token):
    return [t.i for t in token.subtree]
def generate_word_delete(content):
  doc = nlp(content)
  to_delete = []
  for token in doc:
    if token.dep_ in ["amod", "nummod", "advmod", "nmod", "npadvmod", "relcl", "acl", "prep"]:
        if random.random() < 0.5:  # 调整这个概率以满足你的需求
            subtree_indices = [t.i for t in token.subtree]
            to_delete.extend(subtree_indices)
  Token.set_extension("keep", default=True, force=True)
  processed_text = " ".join([token.text_with_ws for i, token in enumerate(doc) if i not in to_delete]).rstrip()
  return processed_text

def generate_word_swap(content):

  L1= nlp(content)
  sentences = [sent.text for sent in L1.sents]
  text = ""
  client = OpenAI()
  for sentence in sentences:
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Find the subject and predicate in the sentence, switch them positions, and then reconstruct them into a readable and understandable sentence"},
            {"role": "user", "content": sentence},
        ]
    )
    result = completion.choices[0].message.content
    text += result 
  return text

def generate_check(content):
  client = OpenAI()
  completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Check if the content is grammatically correct and make any necessary changes to ensure it is grammatically correct. And then reconstruct the content into a readable and understandable content."},
            {"role": "user", "content": content},
        ]
    )
  result = completion.choices[0].message.content
  result = ' '.join(sentence.strip() for sentence in result.split('\n') if sentence.strip())
  return result


content = "The city recorded its rainiest day ever on Monday, and it wasn't better news for the rest of California either. A state of emergency was declared and evacuation orders were issued. Mudslides hit neighbourhoods, drivers were stranded, and half a million residents lost power. About 37 million residents, or 94% of the state's population, are under flood alerts. The already-deadly storm is caused by an atmospheric river, a corridor of water vapour in Earth's lower atmosphere which is carried along by the wind, forming long currents – a kind of sky river. The consequences can be dramatic. The precipitation that falls is comparable to the rain brought by hurricanes making landfall on the Gulf Coast. Climate change is increasing the risk of a California megaflood, Swain's study warns. This extreme storm scenario would produce runoffs 200-400% greater than anything seen before in the Sierra Nevada, the sprawling 400-mile (650km) mountain range that traverses 24 of the 58 counties in California. The last such megaflood happened in 1861, inundating a 300 mile-long (483km) stretch of the Central Valley and large portions of modern-day Los Angeles with water. It could happen again, any time. And, the extremity of such a flood is increased by around 10% per 1C of global warming, because the warmer the planet the more capacity the atmosphere has to hold water vapour."
nltk.download('wordnet')
nlp = spacy.load("en_core_web_sm")


newContent = generate_random_citiesAndCountries(content)
# print(" ")
# print("New Content: ", newContent)
# print(" ")
newContent = generate_random_weekdays(newContent)
# print(" ")
# print("New Content: ", newContent)
# print(" ")
newContent = generate_random_date(newContent)
# print(" ")
# print("New Content: ", newContent)
# print(" ")
newContent = generate_random_numbers(newContent)
# print(" ")
# print("New Content: ", newContent)
# print(" ")
newContent = generate_random_quantifiers(newContent)
# print(" ")
# print("New Content: ", newContent)
# print(" ")
newContent = generate_antonyms(newContent)
# print(" ")
# print("New Content: ", newContent)
# print(" ")
newContent = generate_NONE_NEGATIVE_words(newContent)
# print(" ")
# print("New Content: ", newContent)
# print(" ")
newContent = generate_word_delete(newContent)
# print(" ")
# print("New Content: ", newContent)
# print(" ")
newContent = generate_word_swap(newContent)
# print(" ")
# print("New Content: ", newContent)
# print(" ")
newContent = generate_check(newContent)
# print(" ")
#print("New Content: ", newContent)

