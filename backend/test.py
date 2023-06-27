from fastapi.testclient import TestClient
import json

from main import botbuster

client = TestClient(botbuster)


def test_create_item():
    response = client.post(
        "/checktext/",
        json={
            "list_of_apis": ['Writer', 'Sapling AI', 'Hugging Face'],
            "text": "Singapore Polytechnic (SP) is a renowned institution offering a diverse range of diploma courses and fostering a culture of academic excellence, practical learning, and industry partnerships. With state-stry attachments to prepare graduates for successful careers. SP also encoof-the-art facilities and dedicated faculty, SP equips students with the skills and knowledge needed for their chosen fields. The institution emphasizes experiential learning, project-based education, and induurages innovation, entrepreneurship, and holistic development through its vibrant campus life and co-curricular activities. Overall, Singapore Polytechnic is a leading institution that provides a comprehensive and dynamic educational experience to shape the future professionals of Singapore."
        },
    )
    assert response.status_code == 200

# test_create_item()


def check_sms():
    response = client.get(
        "/webscraper/"
    )
    assert response.status_code == 200

check_sms()

'''
text = "`Singapore Polytechnic (SP) is a renowned institution offering a diverse range of diploma courses and fostering a culture of academic excellence, practical learning, and industry partnerships. With state-of-the-art facilities and dedicated faculty, SP equips students with the skills and knowledge needed for their chosen fields. The institution emphasizes experiential learning, project-based education, and industry attachments to prepare graduates for successful careers. SP also encourages innovation, entrepreneurship, and holistic development through its vibrant campus life and co-curricular activities. Overall, Singapore Polytechnic is a leading institution that provides a comprehensive and dynamic educational experience to shape the future professionals of Singapore.`"
results = [
                    {
                        "generated_prob": 0,
                        "perplexity": 34,
                        "sentence": "Singapore Polytechnic (SP) is a renowned institution offering a diverse range of diploma courses and fostering a culture of academic excellence, practical learning, and industry partnerships."
                    },
                    {
                        "generated_prob": 0,
                        "perplexity": 19,
                        "sentence": "With state-of-the-art facilities and dedicated faculty, SP equips students with the skills and knowledge needed for their chosen fields."
                    },
                    {
                        "generated_prob": 0,
                        "perplexity": 58,
                        "sentence": "The institution emphasizes experiential learning, project-based education, and industry attachments to prepare graduates for successful careers."
                    },
                    {
                        "generated_prob": 0,
                        "perplexity": 39,
                        "sentence": "SP also encourages innovation, entrepreneurship, and holistic development through its vibrant campus life and co-curricular activities."
                    },
                    {
                        "generated_prob": 0,
                        "perplexity": 42,
                        "sentence": "Overall, Singapore Polytechnic is a leading institution that provides a comprehensive and dynamic educational experience to shape the future professionals of Singapore."
                    }
                ]
      
scores = {
    "general_score": {},
    "sentence_score": []
}

for sentence in text.split("."):
    sentence =  sentence.strip() + "."
    if sentence == ".":
        continue
    scores["sentence_score"].append({f"{sentence}": {"highlight": 0, "api": []}})
for num in range(0, len(results)):
    for key in scores["sentence_score"][num].keys():
        print(key, results[num]["sentence"], key == results[num]["sentence"], sep ="\n")

print(scores)
'''