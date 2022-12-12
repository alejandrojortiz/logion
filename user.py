from flask_login import UserMixin
import server_api
class User(UserMixin):
    def __init__(self, user_id, name, email, institution, position, ip_address):
        self.id = user_id
        self.name = name
        self.email = email
        self.institution = institution
        self.position = position
        self.ip_address = ip_address

    @staticmethod
    def get(user_id):
        user = server_api.get_user(user_id)
        if not user:
            return None

        user = User(
            user_id=user_id, name=user['name'], email=user['email'], institution=user['institution'],
            position=user['position'], ip_address=user['ip_address']
        )
        return user

    @staticmethod
    def create(user_id, name, email, institution, position, ip_address):
        server_api.add_account({
            'user_id': user_id, 'name': name, 'email': email,
            'institution': institution, 'position': position, 'ip_address': ip_address
        })