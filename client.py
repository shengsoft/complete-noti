# from marshmallow import Schema, fields, post_load
from datetime import datetime
import uuid
from database import Database



class Client:


    # def __init__(
    #     self,
    #     first_name: str, 
    #     last_name: str,
    #     email: str,
    #     ssn: str,
    #     image: str,
    #     administrator_id: str,
    #     date_of_birth: str = None,
    #     _id: str = None, 
    #     middle_name: str = None):

    #     self._id = _id or uuid.uuid4().hex
    #     self.first_name = first_name
    #     self.middle_name = middle_name or 'n/a'
    #     self.last_name = last_name
    #     self.email = email
    #     self.date_of_birth =  datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    #     self.ssn = ssn
    #     self.image = image
    #     self.administrator_id = administrator_id



    # def client_schema(schema):
    # #     class ClientSchema(Schema):
    # #         _id = fields.Str()
    # #         first_name = fields.Str()
    # #         middle_name = fields.Str()
    # #         last_name = fields.Str()
    # #         email = fields.Str()
    # #         date_of_birth = fields.Date()
    # #         ssn = fields.Str()
    # #         image = fields.Str()
    # #         administrator_id = fields.Str()
    # #         expenses = fields.Dict(keys=fields.Str(), values=fields.Nested(schema) )

    # # @post_load
    # # def make_client(self, data, **kwargs):
    # #     return Client(**data)  

    

    
    def get_all_clients(client_ids):
        clients = []
        if client_ids is not None:
            for client_id in client_ids:
                c = Database.get_records('client', {'_id' : ObjectId(client_id)})
                clients.append(c) 
        return clients

    def get_client_by_payee(id):
        client = client_collection.find({'administrator_id' : id})
        return client    

    def budget_calculator(value_list):
        return sum(value_list)  
