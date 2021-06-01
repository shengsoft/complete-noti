import random
import json
from datetime import date, datetime
from json import JSONEncoder

class Generator:
    def generate_code(password_length):
        characters = '01234567890abcdefghijklmnopqrstuvwxyzABCDFEGHIJKLMNOPQRSTUVWXYZ'
        code = ''.join(random.choice(characters) for _ in range(password_length))
        return code
    
    def generate_report():
        #generates an annual or weeky report (date can be changed to schedule an annual report from a date passed in)
        pass


class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()



