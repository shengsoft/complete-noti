from marshmallow import Schema, fields, post_load
# from client import client_schema
import uuid

class Payee:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        image: str,
        _id: str = None,
        middle_name: str = None):


        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.image = image
        self._id = _id or uuid.uuid4().hex
        self.middle_name = middle_name or 'n/a'

