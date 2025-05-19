from django.contrib.auth.models import User

user = User.objects.create_superuser(
    username='sss',
    email='sss@example.com',
    password='sss'
)
