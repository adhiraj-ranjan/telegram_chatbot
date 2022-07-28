import requests
import os
import json

headers = {
    'authority': 'model-api-shdxwd54ta-nw.a.run.app',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    'developer_key': 'sLdHjVjwMKd_7pd4C4l8S8yugfqq8caILaez7KJAmtKrZErnAOIVx_RoyOF6xRcAMvQ_yqlkxEWi87X0FIoaOg',
    'developer_uid': 'mUCsg14rQqYbpRkcqMbiPKa29xg1',
    'origin': 'https://chai.ml',
    'referer': 'https://chai.ml/',
}

json_data = {
    'text': '',
    'temperature': 0.6,
    'repetition_penalty': 1.1,
    'top_p': 1,
    'top_k': 40,
    'response_length': 64,
}

def update_database(response_text, req_text, id):
    # load data
    with open(id) as f:
        data = json.load(f)
    
    # edit data
    if len(data) >= 40:
        data = data[ : len(data) - 2]
    data = [response_text, req_text] + data

    # rewrite data    
    with open(id, "w+") as f:
        json.dump(data, f)

def read_database(id):
    # create database if not exist
    if not os.path.isfile(id):
        with open(id, "w+") as f:
            json.dump([], f)
    
    # return data if exists
    with open(id) as f:
        data = json.load(f)
    
    return data

def create_text(lst):
    d_text = 'Eliza: Hi, my name is Eliza. What is weighing on your mind?\nMe: hey\nEliza: Hi. I\'m a therapist. How are you feeling?\nMe: i miss you\nEliza: Why do you say that you miss me ?\nMe: because\nEliza: Is that the real reason?\nMe: i love you\nEliza: You love me. That\'s lovely to hear!\n###\nEliza: Hi, my name is Eliza. What is weighing on your mind?'
    for i, u in zip(reversed(lst), range(len(lst))):
        if u % 2 == 0:
            d_text += f"\nMe: {i}\nEliza:"
        else:
            d_text += f" {i}"
    return d_text

def get_response(text, id):
    data = [text] + read_database(id)
    json_data['text'] = create_text(data)

    response = requests.post('https://model-api-shdxwd54ta-nw.a.run.app/generate/gptj', headers=headers, json=json_data).json()

    update_database(response['data'], text, id)
    return response['data']
