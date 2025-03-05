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
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = False  # Make sure SSL is off since we're using TLS
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'djangohive75@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'bvga dznf nvwk uqew')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIMEOUT = 30  # Add timeout setting