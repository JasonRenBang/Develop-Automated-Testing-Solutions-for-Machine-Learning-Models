from openai import OpenAI
import spacy
from sentence_transformers import SentenceTransformer, util
import config

topics = []
originals = []
paraphrases = []
manualTransformations = []

with open('dataOPandM.txt', 'r', encoding='utf-8') as file:
    currentTopic = ''
    currentOriginal = ''
    currentParaphrase = ''
    currentManualTransformation = ''
    mode = 'TOPIC' #chase the current data mode: topic, original, paraphrase, manualTransformation
    for line in file:
        line = line.strip()
        if line.startswith('Topic:'):
            if currentTopic !='':
                topics.append(currentTopic)
                originals.append(currentOriginal)
                paraphrases.append(currentParaphrase)
                manualTransformations.append(currentManualTransformation)

                currentOriginal = ''
                currentParaphrase = ''
                currentManualTransformation = ''
            currentTopic = line[len('Topic: '):]
            mode = 'TOPIC'
        elif line=='Original paragraph':
            mode = 'ORIGINALPARAGRAPH'
        elif line=='Paraphrased paragraph':
            mode = 'PARAPHRASEDPARAGRAPH'
        elif line=='Manual transformation':
            mode = 'MANUALTRANSFORMATION'
        else:
            if mode=='ORIGINALPARAGRAPH':
                currentOriginal += line
            elif mode=='PARAPHRASEDPARAGRAPH':
                currentParaphrase += line
            elif mode=='MANUALTRANSFORMATION':
                currentManualTransformation += line
    if currentTopic !='':
        topics.append(currentTopic)
        originals.append(currentOriginal.strip())
        paraphrases.append(currentParaphrase.strip())
        manualTransformations.append(currentManualTransformation.strip())

entities = []
for i in range(len(topics)):
    topic = topics[i]
    content1 = originals[i]
    content2 = paraphrases[i]
    content3 = manualTransformations[i]
    entities.append((topic, content1, content2, content3))

numOfSentences = config.NUMBER_OF_SUMMARY_SENTENCES
wordLimit = config.WORD_LIMIT_FOR_EACH_SENTENCE

for entity in entities:
    topic = entity[0]
    original = entity[1]
    paraphrase = entity[2]
    manualTransformation = entity[3]


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
                {"role": "user", "content": manualTransformation},
            ]
        )
    sum3 = completion2.choices[0].message.content

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

    cosine_scoresppp = util.pytorch_cos_sim(embeddings1, embeddings3)
    matched_sentences_and_scores_ppp = []
    for i in range(len(sentences1)):
        best_match_idx  = cosine_scoresppp[i].argmax().item()
        best_score = cosine_scoresppp[i][best_match_idx].item()
        matched_pair = (sentences1[i], sentences3[best_match_idx], best_score)
        matched_sentences_and_scores_ppp.append(matched_pair)

    resultspp = []
    for pair in matched_sentences_and_scores_pp:
        sentence1 = pair[0]
        sentence2 = pair[1]
        completion4 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Could you tell me if these two sentences are contradicting each other."},
                {"role": "user", "content": sentence1},
                {"role": "user", "content": sentence2}
            ]
        )
        result = completion4.choices[0].message.content
        resultspp.append((sentence1,sentence2,result))

    resultsppp = []
    for pair in matched_sentences_and_scores_ppp:
        sentence1 = pair[0]
        sentence2 = pair[1]
        completion5 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Could you tell me if these two sentences are contradicting each other."},
                {"role": "user", "content": sentence1},
                {"role": "user", "content": sentence2}
            ]
        )
        result = completion5.choices[0].message.content
        resultsppp.append((sentence1,sentence2,result))

    print("Topic: ", topic)
    print("  ")
    print("results for ppp", resultsppp)

      







