import database import Database

class Authenticate:
    def verify_account(collection, email):
        #check the db for the email address
        admin_email = Database.get_record(collection, {'email' : email})
        # client_email = clients.find_one({'email' : email})
        if admin_email is None:
            print('Unauthorized')
        else:
            send_passcode(email)  


    def expire_passcode():
        #after 10 minutes of sending the code expire it
        pass


    
