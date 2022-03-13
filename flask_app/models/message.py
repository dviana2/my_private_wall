from flask_app.config.mysqlconnection import connectToMySQL

db= 'private_wall2'

class Message:
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.sender = data['sender']
        self.sender_id = data['sender_id']
        self.receiver = data ['receiver']
        self.receiver_id = data ['receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_user_messages(cls,data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE users2.id =  %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        messages = []
        for message in results:
            messages.append( cls(message) )
        return messages


    # @classmethod
    # def get_all_user_messages(cls,data):

    #     # query = "SELECT * from messages "
    #     query = "SELECT * from messages join users on users.id = messages.user_id" # we do a regular join because we know every messages posted will have a sender
    #     results = connectToMySQL(db).query_db(query,data) #data coming back to us
    #     messages = []
    #     for message in results:
    #         messages.append(cls(message))
    #     return messages

    @classmethod
    def save(cls,data):
        query = "INSERT INTO messages (content,sender_id,receiver_id) VALUES (%(content)s,%(sender_id)s,%(receiver_id)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy_message(cls,data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)