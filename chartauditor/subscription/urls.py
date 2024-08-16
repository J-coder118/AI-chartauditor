from django.urls import path
from chartauditor.subscription import views

urlpatterns = [
    path('payment-plans/', views.SubscriptionPlanView.as_view(), name='payment_plans'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('webhook/', views.stripe_webhook),
]
