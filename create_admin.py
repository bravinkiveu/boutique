import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
email = 'bravinkiveu@gmail.com'
password = 'Mukongolo'
if User.objects.filter(username=username).exists():
    u = User.objects.get(username=username)
    u.email = email
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print('Superuser updated:', username)
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superuser created:', username)
