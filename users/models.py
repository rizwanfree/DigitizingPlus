from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The User ID field must be set')
        
        # Normalize and validate emails if provided
        if 'email' in extra_fields:
            extra_fields['email'] = self.normalize_email(extra_fields['email'])
        if 'email2' in extra_fields:
            extra_fields['email2'] = self.normalize_email(extra_fields['email2'])
        if 'email3' in extra_fields:
            extra_fields['email3'] = self.normalize_email(extra_fields['email3'])
        
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(user_id, password, **extra_fields)

class User(AbstractUser):
    COUNTRY_CHOICES = [
        ('United States', 'United States'),
        ('United Kingdom', 'United Kingdom'),
        ('Australia', 'Australia'),
        ('New Zealand', 'New Zealand'),
        ('Germany', 'Germany'),
        ('Canada', 'Canada'),
    ]
    
    username = None
    user_id = models.CharField(max_length=100, unique=True, blank=False, null=False)
    
    # Main email field (now optional)
    email = models.EmailField()
    # Additional email fields
    email2 = models.EmailField(blank=True, null=True, verbose_name="Secondary Email")
    email3 = models.EmailField(blank=True, null=True, verbose_name="Tertiary Email")
    
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=15)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    country = models.CharField(
        max_length=15,
        choices=COUNTRY_CHOICES,
        default='US',  # Default to United States
        verbose_name="Country"
    )

    # Use user_id as the login field instead of email
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []  # Removed email from required fields

    objects = UserManager()

    COUNTRY_CODE_MAP = {
        'United States': 'us',
        'United Kingdom': 'gb',
        'Australia': 'au',
        'New Zealand': 'nz',
        'Germany': 'de',
        'Canada': 'ca',
    }
    
    @property
    def country_code(self):
        return self.COUNTRY_CODE_MAP.get(self.country, '')

    def __str__(self):
        return self.user_id

    def get_all_emails(self):
        """Return all non-empty email addresses associated with the user"""
        return [email for email in [self.email, self.email2, self.email3] if email]
    


class CreditCard(models.Model):
    CARD_TYPE_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('amex', 'American Express'),
        ('discover', 'Discover'),
    ]

    COUNTRY_CHOICES = [
        ('USA', 'United States'),
        ('UK', 'United Kingdom'),
        ('Australia', 'Australia'),
        ('France', 'France'),
        ('Germany', 'Germany'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_cards')
    name_on_card = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20)
    expiry_month = models.IntegerField()
    expiry_year = models.IntegerField()
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES)
    verification_code = models.CharField(max_length=10)  # Usually CVV/CVC

    # Contact Info
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()

    # Billing Address
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)

    added_at = models.DateTimeField(auto_now_add=True)

    def masked_number(self):
        return f"**** **** **** {self.card_number[-4:]}"

    def __str__(self):
        return f"{self.user.user_id} - {self.card_type.upper()} ({self.masked_number()})"
