from django.db import models

# Create your models here.
from django.db.models import Model
from django.db.models.fields import IntegerField, TextField, CharField, TimeField, DateTimeField, BooleanField


class MessageLog(Model):
    sms_id = IntegerField(blank=True, null=True)
    via_gate = CharField(max_length=40)
    sender = CharField(max_length=50)
    recepient = CharField(max_length=50)
    time = DateTimeField(auto_now=True)
    sent_ok = BooleanField()
    error_description = TextField(max_length=1500, blank=True, null=True)
