DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'secondary': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_secondary_database_name',
        'USER': 'Carson_Pugh',
        'PASSWORD': '12345',
        'HOST': '192.168.56.1',  # Use the correct IP address here
        'PORT': '3306',
    }
}