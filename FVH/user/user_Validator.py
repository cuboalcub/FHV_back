from django.contrib.auth.models import User
from IValidator import IValidator

class UserValidator(IValidator):
     def __init__(self):
        super().__init__(User)
