from django.core.mail import send_mail
from django.conf import settings
import stripe


def email_confirmation(email, uuid, host):
    subject = 'ChartChecker Verification Email'
    message = f'Please click on the link below to verify your email {host}accounts/{uuid}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def create_stripe_customer(user):
    try:
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        response = stripe.Customer.create(
            email=user.email,
        )
        user.stripe_customer_id = response['id']
        user.save()
        print('Stripe customer created:', response['id'])
    except Exception as e:
        print('Error creating Stripe customer:', str(e))
