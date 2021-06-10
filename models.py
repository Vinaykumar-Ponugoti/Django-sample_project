from django.db import models

# Create your models here.
class Parkslots(models.Model):
    carid = models.CharField(max_length=10)
    phnnum = models.IntegerField()
    rownum = models.IntegerField()
    colnum = models.IntegerField()
    status = models.IntegerField()
    checkin = models.TimeField(auto_now=True)
    def __str__(self):
        return "carid:{} mobile:{} row:{} col:{} status:{} checkedin at:{}".format(self.carid,self.phnnum,self.rownum,self.colnum,self.status,self.checkin)


class Freeslots(models.Model):
    rowval = models.IntegerField()
    colval = models.IntegerField()
    status = models.IntegerField()
    def __str__(self):
        return "%d %d %d" % (self.rowval,self.colval,self.status)
    class Meta:
        db_table = 'Freeslots'
        unique_together = (('rowval', 'colval'),)


class Workers(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Bookauth(models.Model):
    carid = models.CharField(max_length=10)
    phnnum = models.IntegerField()
    otp = models.IntegerField()

    def __str__(self):
        return "carid:{} mobile:{} otp:{}".format(self.carid,self.phnnum,self.otp)
