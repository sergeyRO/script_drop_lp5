import requests
import json
import math

def drop_faces(json_list):
    headers = {"Luna-Account-Id": json_list['Luna-Account-Id'], "Content-Type": json_list['Content-Type']}
    host = f"{json_list['protocol']}://{json_list['host']}:{json_list['port']}"
    url = f"{host}/6/tasks/gc"
    data = {
        "account_id": json_list['Luna-Account-Id'],
        "description": "Drop_face",
        "content": {"target": "events", "remove_samples": True}
    }
    requests.post(url, headers=headers, data=json.dumps(data))

    url = f"{host}/6/faces/count"
    faces_count = requests.get(f"{url}?list_id={json_list['list_id']}&targets={json_list['targets']}").json()['faces_count']
    ost_range = math.ceil(faces_count/100)

    face_ids = []
    count_face = 0
    while ost_range != 0:

        url = f"{host}/6/faces"
        responce_faces = requests.get(f"{url}?list_id={json_list['list_id']}&targets={json_list['targets']}&page={ost_range}&page_size={json_list['page_size']}").json()['faces']

        for face in responce_faces:
            for val in face.values():
                face_ids.append(val)
                count_face += 1

        if count_face >= 900:
            data = {'face_ids': face_ids}
            requests.delete(url, headers=headers, data=json.dumps(data))
            face_ids = []
            count_face = 0
        ost_range -= 1
    data = {'face_ids': face_ids}
    requests.delete(url, headers=headers, data=json.dumps(data))
    return True

if __name__ == '__main__':
    with open('options.json') as file:
        json_list = json.load(file)
    print(drop_faces(json_list))
    exit()
