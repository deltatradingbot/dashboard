from django.db import models

# Create your models here.

class PaymentModal(models.Model):
    user_id = models.IntegerField()
    pay_id = models.CharField(max_length=100)
    latest_pay = models.DateField()
    verified = models.IntegerField(default=0)

    def __str__(self):
        return "user : " + str(self.user_id) + "  |  " + "Ref ID : " + str(self.pay_id) + "  |  " + "Date : " + str(self.latest_pay) + " | verified : " + str(self.verified)

class SignalsModal(models.Model):
    signals_text = models.TextField()
