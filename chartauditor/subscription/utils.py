from chartauditor.subscription.models import Subscription
from chartauditor.accounts.models import User
from chartauditor.pdf_wrapper.models import ChartChecker
from chartauditor.pdf_wrapper.utils import update_chart_obj_status


def create_subscription(chart_id, user_id, client_secret):
    chart = ChartChecker.objects.get(id=chart_id)
    user = User.objects.get(id=user_id)
    subscription = Subscription.objects.create(
        user=user,
        client_secret=client_secret,
    )
    subscription.save()
    update_chart_obj_status(chart, user)
    return subscription
