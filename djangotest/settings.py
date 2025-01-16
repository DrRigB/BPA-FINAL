DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'root',  # Database name
        'USER': 'root',  # MySQL username
        'PASSWORD': 'RootPass1.49',  # MySQL password
        'HOST': '0.0.0.0',  # Allow connections from any IP address
        'PORT': '3306',  # Default MySQL port
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'djangohive75@gmail.com'
EMAIL_HOST_PASSWORD = 'bvga dznf nvwk uqew'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER