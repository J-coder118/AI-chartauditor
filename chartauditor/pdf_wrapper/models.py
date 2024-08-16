from django.db import models
from chartauditor.accounts.models import User

# Create your models here.


class ChartChecker(models.Model):
    AETNA = 'Aetna'
    CIGNA = 'Cigna'

    COMPLIANCE = (
        (AETNA, 'Aetna'),
        (CIGNA, 'Cigna'),
    )

    FLORIDA = 'Florida'
    CALIFORNIA = 'California'

    STATE_COMPLIANCE = (
        (FLORIDA, 'Florida'),
        (CALIFORNIA, 'California'),
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    chart = models.FileField(upload_to='charts')
    chart_name = models.CharField(max_length=200, null=True, blank=True)
    clean_chart = models.JSONField()
    total_page_count = models.IntegerField(null=True, blank=True)
    character_count = models.IntegerField(null=True, blank=True)
    score = models.CharField(max_length=100, null=True, blank=True)
    chart_response = models.TextField(null=True, blank=True)
    chart_price = models.FloatField(null=True, blank=True)
    is_payment_done = models.BooleanField(default=False)
    is_report_emailed = models.BooleanField(default=False)
    is_state_compliance = models.BooleanField(default=False)
    state_compliance = models.CharField(max_length=200, null=True, blank=True, choices=STATE_COMPLIANCE)
    is_CARF_compliance = models.BooleanField(default=False)
    is_marked_cover_letter = models.BooleanField(default=False)
    is_commission_compliance = models.BooleanField(default=False)
    is_insurance_compliance = models.BooleanField(default=False)
    insurance_compliance = models.CharField(max_length=200, null=True, blank=True, choices=COMPLIANCE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    dob = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    mr_number = models.CharField(max_length=200, null=True, blank=True)
    is_ss_number = models.BooleanField(default=False)
    ss_number = models.CharField(max_length=200, null=True, blank=True)
    is_driving_license = models.BooleanField(default=False)
    driving_license = models.CharField(max_length=200, null=True, blank=True)
    is_address = models.BooleanField(default=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    is_credit_card = models.BooleanField(default=False)
    credit_card = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)