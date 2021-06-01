


class Chat:
    def __init__(self, payee_id: str, client_id: str, messages):
        self.payee_id = payee_id
        self.client_id = client_id
        self.messages = messages


    def get_latest_message():
        #gets most recent message (this is for the payee dashboard)
        pass

    def get_chat_archive():
        #get chat history between a payee and a particular client
        pass

    def auto_save():
        #auto_save will save chat log after a period of time
        pass

    def send_notification():
        #notify user(client or payee) that a message has been sent to them
        pass

    def save_room():
        pass


    def get_room():
        pass


    def add_member():
        pass

    def generate_unique_chatroom():
        return Generator.generate_code(24)

    

