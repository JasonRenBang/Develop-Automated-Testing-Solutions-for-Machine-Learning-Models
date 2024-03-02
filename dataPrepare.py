from openai import OpenAI
import spacy
from sentence_transformers import SentenceTransformer, util
import config

topics = []
contents = []

with open('paragraphysData2.txt', 'r', encoding='utf-8') as file:
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

for i in range(len(topics)):
    with open('dataOandP.txt', 'a',encoding='utf-8') as file:
        file.write('Topic: ' + topics[i] + '\n')
        file.write('  \n')
        file.write('Original paragraph  \n')
        file.write(contents[i] + '\n')
        file.write('  \n')
        file.write('Paraphrased paragraph  \n')
        file.write(paraphrases[i]+ '\n')
        file.write('  \n')
