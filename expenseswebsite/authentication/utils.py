from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type #for compability

class TokenCreator(PasswordResetTokenGenerator): #makes sure user not using the same link to reset password
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))
    
token_generator=TokenCreator()