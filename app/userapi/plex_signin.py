from urllib import urlencode

import requests



def get_goto_url(user):
    client_identifier = str(user.token.client_identifier)
    get_pin = requests.post('https://plex.tv/api/v2/pins?strong=true',
                            headers=get_headers(client_identifier))

    pin = get_pin.json()

    goto = 'http://app.plex.tv/auth#'
    goto = '%s?%s' % (goto, urlencode({
        'clientID': client_identifier,
        'pinId': pin['id'],
        'code': pin['code'],
        'context[device][product]': 'PlexMyCloud',
        'context[device][platform]': 'Windows_NT',
        'context[device][platformVersion]': '10.0.16299',
        'context[device][version]': '1.0.0',
        'forwardUrl': 'http://localhost:5000/plex_forward/%i' % pin['id']
    }))

    return goto


def get_plex_token(pin_id, user):
    client_identifier = str(user.token.client_identifier)
    poll_pin = 'https://plex.tv/api/v2/pins/{pin}'.format(pin=pin_id)

    poll_pin_request = requests.get(poll_pin,
                                    headers=get_headers(client_identifier))

    poll_pin = poll_pin_request.json()
    plex_token = poll_pin['authToken']

    return plex_token


def get_headers(client_identifier):
    return {
        'X-Plex-Client-Identifier': client_identifier,
        "X-Plex-Product": 'PlexMyCloud',
        "X-Plex-Version": "3",
        'Accept': 'application/json'
    }
