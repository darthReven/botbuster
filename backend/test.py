from fastapi.testclient import TestClient
import json

from main import botbuster

client = TestClient(botbuster)


def test_create_item():
    response = client.post(
        "/checktext/",
        json={
            "list_of_apis": ['Writer', 'Sapling AI', 'Hugging Face'],
            "text": "Singapore Polytechnic (SP) is a renowned institution offering a diverse range of diploma courses and fostering a culture of academic excellence, practical learning, and industry partnerships. With state-of-the-art facilities and dedicated faculty, SP equips students with the skills and knowledge needed for their chosen fields. The institution emphasizes experiential learning, project-based education, and industry attachments to prepare graduates for successful careers. SP also encourages innovation, entrepreneurship, and holistic development through its vibrant campus life and co-curricular activities. Overall, Singapore Polytechnic is a leading institution that provides a comprehensive and dynamic educational experience to shape the future professionals of Singapore."
            },
    )
    assert response.status_code == 200

test_create_item()


def check_text_test():
    response = client.post(
        "c"
    )