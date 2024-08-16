from django.http.response import JsonResponse, HttpResponse
from chartauditor.accounts.decorators import profile_completion_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from chartauditor.subscription.utils import create_subscription
from chartauditor.pdf_wrapper.models import ChartChecker
from django.views.generic.base import TemplateView
from django.conf import settings
import stripe


@method_decorator(profile_completion_required, name='dispatch')
class SubscriptionPlanView(LoginRequiredMixin, TemplateView):
    template_name = 'subscription/plans.html'


@csrf_exempt
def create_payment_intent(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    chart_obj = ChartChecker.objects.filter(user=request.user.id).last()
    amount = int((chart_obj.chart_price) * 100)
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            customer=request.user.stripe_customer_id,
            automatic_payment_methods={"enabled": True},
            metadata={
                "chart_id": chart_obj.id,
                "user_id": request.user.id,
            },

        )
        return JsonResponse({
            'clientSecret': intent['client_secret'],
            'chartId': intent['metadata']['chart_id']
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    print('working webhooks')
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['data']['object']['status'] == 'succeeded':
        chart_id = event['data']['object']['metadata']['chart_id']
        user_id = event['data']['object']['metadata']['user_id']
        client_secret = event['data']['object']['client_secret']
        create_subscription(chart_id, user_id, client_secret)

    return HttpResponse(status=200)
