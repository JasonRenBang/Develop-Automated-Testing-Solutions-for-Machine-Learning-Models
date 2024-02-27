from openai import OpenAI
import spacy
from sentence_transformers import SentenceTransformer, util
import config



topics = []
paragraphs1 = []
paragraphs2 = []
with open('demoParagraphsData.txt', 'r', encoding='utf-8') as file:
    currentTopic = ''
    currentParagraph1 = ''
    currentParagraph2 = ''
    mode = 'TOPIC' #chase the current data mode: topic, paragraph1, paragraph2
    for line in file:
        line = line.strip()
        if line.startswith('Topic:'):
            if currentTopic !='':
                topics.append(currentTopic)
                paragraphs1.append(currentParagraph1)
                paragraphs2.append(currentParagraph2)

                currentParagraph1 = ''
                currentParagraph2 = ''
            currentTopic = line[len('Topic: '):]
            mode = 'TOPIC'
        elif line=='Paragraph1:':
            mode = 'PARAGRAPH1'
        elif line=='Paragraph2:':
            mode = 'PARAGRAPH2'
        else:
            if mode=='PARAGRAPH1':
                currentParagraph1 += line
            elif mode=='PARAGRAPH2':
                currentParagraph2 += line
    if currentTopic !='':
        topics.append(currentTopic)
        paragraphs1.append(currentParagraph1.strip())
        paragraphs2.append(currentParagraph2.strip())

print(topics)

entities = []
for i in range(len(topics)):
    topic = topics[i]
    content1 = paragraphs1[i]
    content2 = paragraphs2[i]
    entities.append((topic, content1, content2))

contentScale = config.CONTENT_SCALE
numOfSentences = config.NUMBER_OF_SUMMARY_SENTENCES
wordLimit = config.WORD_LIMIT_FOR_EACH_SENTENCE



for entity in entities:
    topic = entity[0]
    content1 = entity[1]
    content2 = entity[2]
    
    with open('outcomes2.txt', 'a',encoding='utf-8') as file:
        file.write('--------------------------------------------------------------\n')
        file.write('Topic: ' + topic + '\n')
        file.write('  \n')
        file.write('The two paragraphs are:\n')
        file.write('Paragraph1  \n')
        file.write(content1 + '\n')
        file.write('  \n')
        file.write('Paragraph2  \n')
        file.write(content2 + '\n')
        file.write('  \n')
    
    if len(content1)>contentScale:
        content1 = content1[:contentScale]   
    if len(content2)>contentScale:
        content2 = content2[:contentScale]    
    client = OpenAI()
    completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Could you help me summarize this paragraph in " + str(numOfSentences)+ " short sentences within the word limit of "+ str(wordLimit)},
                {"role": "user", "content": content1},
            ]
        )
    sum1 = completion.choices[0].message.content

    completion2 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Could you help me summarize this paragraph in " + str(numOfSentences)+ " short sentences within the word limit of "+ str(wordLimit)},
                {"role": "user", "content": content2},
            ]
        )
    sum2 = completion2.choices[0].message.content

    # print(sum1)
    # print(" ")
    # print(sum2)
    # print(" ")
    with open('outcomes2.txt', 'a',encoding='utf-8') as file:
        file.write('Their summary produced by ChatGPT are:\n')
        file.write('Summary1:  \n')
        file.write(sum1 + '\n')
        file.write('  \n')
        file.write('Summary2:  \n')
        file.write(sum2 + '\n')
        file.write('  \n')



    nlp = spacy.load("en_core_web_sm")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    L1= nlp(sum1)
    sentences1 = [sent.text for sent in L1.sents]

    L2= nlp(sum2)
    sentences2 = [sent.text for sent in L2.sents]

    # print(sentences1)
    # print(" ")
    # print(sentences2)
    # print(" ")

    embeddings1 = model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)

    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
    matched_sentences_and_scores = []
    for i in range(len(sentences1)):
        best_match_idx  = cosine_scores[i].argmax().item()
        best_score = cosine_scores[i][best_match_idx].item()
        matched_pair = (sentences1[i], sentences2[best_match_idx], best_score)
        matched_sentences_and_scores.append(matched_pair)


 #   print(matched_sentences_and_scores)
    with open('outcomes2.txt', 'a',encoding='utf-8') as file:
        file.write('After pairing, we have identified the following pairs:\n')
        for i in range(len(matched_sentences_and_scores)):
            file.write('Pair ' + str(i+1) + ':\n')
            
            file.write(matched_sentences_and_scores[i][0] + '\n')
            file.write(' \n')
            file.write(matched_sentences_and_scores[i][1] + '\n')
            file.write(' \n')

    results = []


    for pair in matched_sentences_and_scores:
        sentence1 = pair[0]
        sentence2 = pair[1]
        completion3 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Could you tell me if these two sentences are contradicting each other."},
                {"role": "user", "content": sentence1},
                {"role": "user", "content": sentence2}
            ]
        )
        result = completion3.choices[0].message.content
        results.append((sentence1,sentence2,result))
    
    with open('outcomes2.txt', 'a',encoding='utf-8') as file:
        file.write('The results of the contradiction detection are:\n')
        for i in range(len(results)):
            file.write('Pair ' + str(i+1) + ':')
            file.write(results[i][2] + '\n')
            file.write(' \n')
        file.write('  \n')
    # for item in results:
    #     print(item)
    #     print('')
print('Done, the outcomes2.txt shows the results.')