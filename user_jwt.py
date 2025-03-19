import user_jwt


def createToken(data: dict):
    token: str = user_jwt.encode(payload=data, key='misecret', algorithm='HS256')
    return token