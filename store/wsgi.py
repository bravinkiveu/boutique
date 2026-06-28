import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

# Auto-migrate and create/sync admin superuser on startup/deploy
try:
    import django
    django.setup()
    from django.core.management import call_command
    
    # Run migrations automatically
    print("Running database migrations...")
    call_command('migrate', interactive=False)
    
    # Ensure superuser exists and credentials match 'admin' / 'Mukongolo'
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username = 'admin'
    email = 'bravinkiveu@gmail.com'
    password = 'Mukongolo'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superuser "admin" auto-created successfully.')
    else:
        u = User.objects.get(username=username)
        u.set_password(password)
        u.is_superuser = True
        u.is_staff = True
        u.save()
        print('Superuser "admin" credentials and status synced successfully.')
except Exception as e:
    print('Startup database initialization failed:', e)

application = get_wsgi_application()
