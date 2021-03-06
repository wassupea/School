from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


#authentication of user
class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None,password=None, **kwargs):
       UserModel = get_user_model()
       #fetching the user from the database.
       try:
           user = UserModel.objects.get(email=username)
       except UserModel.DoesNotExist:
            return None
       else:
           if user.check_password(password):
               return user
       return None
