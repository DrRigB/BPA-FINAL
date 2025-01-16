import os
import dj_database_url

# Database configuration
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = False  # Since you're using TLS
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'djangohive75@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'default_password')  # Access password securely
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIMEOUT = 30

# Secret key (ensure this is set in Heroku Config Vars)
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

# Debug setting (ensure this is set to 'False' in Heroku for production)
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
