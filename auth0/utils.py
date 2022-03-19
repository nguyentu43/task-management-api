from django.contrib.auth import authenticate
import json
import jwt
import requests
import os

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
API_IDENTIFIER = os.environ.get('API_IDENTIFIER')


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN)).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    return jwt.decode(token, public_key, audience=API_IDENTIFIER, issuer='https://{}/'.format(AUTH0_DOMAIN),
                      algorithms=['RS256'])


def get_userinfo(token):
    return requests.get('https://{}/userinfo'.format(AUTH0_DOMAIN), headers={'Authorization': token}).json()
