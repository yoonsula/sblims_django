import uuid
from django.db import models

class Equipment(models.Model):
    id = models.UUIDField(primary_key=True, default="Default Value", editable=False)
    equip = models.CharField(max_length=100)
    equip_num = models.PositiveSmallIntegerField()
    subname = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=50)
    serial_no = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    incharge = models.CharField(max_length=50)
    asset_id = models.CharField(max_length=20)
    installed_date = models.CharField(max_length=20)
    account = models.CharField(max_length=50)
    price = models.CharField(max_length=100)
    register_date = models.CharField(max_length=20)
    status = models.PositiveSmallIntegerField()
    

    def __str__(self):
        return self.equip