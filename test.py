import json

def get_final_score(username):
    with open('data/rank/rank.json', 'r') as rank_file:
        data = json.load(rank_file)
    for student in data:
        if student["name"] == username:
            return student["final_score"]
    return None  # Return None if the username is not found



print(get_final_score("kushagra"))