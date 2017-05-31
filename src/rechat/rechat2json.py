import json


def json2json(json):
    general_info = json[0]

    toxic_json = {
        'vod_id': general_info['_id'],
        'title': general_info['title'],
        'game': general_info['game'],
        'channel_name': general_info['channel']['name'],
        'channel_display': general_info['channel']['display_name'],
        'start_timestamp': general_info['start_timestamp']
    }

    messages = []
    for i in range(1, len(json) - 1):
        data = json[i]
        message = {
            'user': data['attributes']['tags']['display-name'],
            'user_id': data['attributes']['tags']['user-id'],
            'message': data['attributes']['message']
        }
        messages.append(message)

    toxic_json['messages'] = messages


def file2json(file_name):
    with open(file_name) as data_file:
        data = json.load(data_file)
    json2json(data)


file2json("rechat-148361448.json")
