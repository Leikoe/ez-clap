import requests
import time
import datetime
import math
import random


def print_sep():
    print("#######################################################################################")

def generate_token():
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
    
    return f"z{math.floor(random.random() * random.random() * unix_timestamp)}"

TOKEN = generate_token()
BEARER = f"bearer {TOKEN}"

print(TOKEN)

QUIZ_ID = ""
if QUIZ_ID == "":
    QUIZ_ID = input("QUIDZ_ID ?\n")

print_sep()

questions = requests.get(f"https://app.wooclap.com/api/events/{QUIZ_ID}", headers={ "authorization": BEARER }).json()
questions = questions["questions"]

def send_answers(question_id, answers):
    print(f"[Ø] Sending {len(answers)} answers.")
    url = f"https://app.wooclap.com/api/questions/{question_id}/push_answer" 
    data = {
        "choices": answers,
        "token": TOKEN
    } 
    print(url)
    print(data)
    res = requests.post(url, data=data, headers={
        "Authorization": BEARER,
        "Content-Type": "application/json"
    }).text
    print(f"[Ø] Sent ! ({res})")

for question in questions[1:]:
    question_type = question["__t"]
    try:
        question_is_correctable = question["correctable"]
    except:
        question_is_correctable = True
    question_id = question["_id"]
    prompt = question["title"]
    print(f"Prompt: {prompt}\n")

    if question_type == "Matching":
        correct_answers = question["matchesDestination"]
        for i, answer in enumerate(correct_answers):
            print(f"Answer #{i} | choice: {answer['text']}")
    elif question_type == "OpenQuestion" and question_is_correctable:
        correct_answers = question["allExpectedAnswers"][0]
        for i, s in enumerate(correct_answers):
            print(f"Answer #{i} | choice: {s}")
    elif question_type == "LabelAnImage":
        correct_answers = question["legends"]
        for i, s in enumerate(correct_answers):
            answer = "'" + "' or '".join(s["synonyms"]) + "'"
            print(f"Answer #{i} | choice: {answer}")
    elif question_type == "MCQ":
        answers = question["choices"]
        correct_answers = []
        for answer in answers:
            choice_id = answer["_id"]
            choice_choice = answer["choice"]
            choice_is_correct = answer["isCorrect"]
            print(f"Answer #{choice_id} | choice: {choice_choice} | isCorrect: {choice_is_correct}")
            if choice_is_correct:
                correct_answers.append(choice_id)
    
    else:
        print("couldn't find answers")
        
        
        #send_answers(question_id, correct_answers)
        #time.sleep(1)
    print_sep()
