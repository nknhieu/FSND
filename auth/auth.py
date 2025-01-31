import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt, jwk
from urllib.request import urlopen
import requests
from jose.utils import base64url_decode

AUTH0_DOMAIN = 'dev-62axng3d8tca4ra1.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'vehicle'

## AuthError Exception
'''
http://localhost:8080/login-results#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlpiajlaMlNNOGRDaHJMbzdvLTl0WCJ9.eyJpc3MiOiJodHRwczovL2Rldi02MmF4bmczZDh0Y2E0cmExLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NGQ1ZmY3Y2IxNjBlMzdjOGMzNmYzZDQiLCJhdWQiOiJ2ZWhpY2xlIiwiaWF0IjoxNjkxODU3NDM2LCJleHAiOjE2OTE4NjQ2MzYsImF6cCI6IkVJQTkxWEozMU1Ec2tkeG5YQXJJRlFKczZ1MGFGUHZUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6dmVoaWNsZSIsInBvc3Q6dmVoaWNsZSJdfQ.awRtSVRXi-o17nIBg58458n7PqJMxeuq2i-dq5we2m-EKqOy2MI4oTDIdxEzLhCurFzaFhojQiuoQ0_Q-fR94sIF_U6Ipj3VZ5X8ccQw0_BL9SJwlNcdw7tqOgF1bJ_jU3hTavuKmTm3wdSZRuOiO9nvqx8QysnieH4kmVV0yJalJcnsBUmdcrmFelmCZzbVOktBt_ZA3wBvsynItZw5SzYwSXyR0MSZg1oFVWa6bAkDw7liXRi0E5K8eishTRYRaWn2abo5u39anXoG15MXJ2Z11FYblcVTlbyGREFlRZTBAynRhhHgXECNoDwHawH-OR7s5tIYIfdSjceXBBuipA&expires_in=7200&token_type=Bearer
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    # raise Exception('Not Implemented')
    auth = request.headers.get('Authorization')

    if not auth:
            raise AuthError({
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected.'
            }, 401)

    parts = auth.split()

    if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must start with "Bearer".'
            }, 401)

    return parts[1]

    
'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    # raise Exception('Not Implemented')
    # Check if permissions array is in the JWT payload
    permissions = payload.get('permissions', [])

    # Check if the specified permission is present in the permissions array
    if permission not in permissions:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found',
        }, 401)

    return True

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    # raise Exception('Not Implemented')
    # Retrieve JWKS (JSON Web Key Set) from the authorization server
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    response = requests.get(jwks_url)
    jwks = response.json()

    # Get the unverified header from the token
    unverified_header = jwt.get_unverified_header(token)

    # Find the appropriate key in JWKS based on the 'kid' (Key ID) from the unverified header
    rsa_key = None
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = jwk.construct(key)
            break

    # Verify and decode the JWT token using the RSA key
    if rsa_key:
        try:
            # Verify the signature and decode the token
            decoded_token = jwt.decode(
                token,
                rsa_key.to_pem(),
                algorithms=ALGORITHMS,
                audience='vehicle',
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return decoded_token

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)
'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
# def requires_auth(permission=''):
#     def requires_auth_decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             token = get_token_auth_header()
#             payload = verify_decode_jwt(token)
#             check_permissions(permission, payload)
#             return f(payload, *args, **kwargs)

#         return wrapper
#     return requires_auth_decorator
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator