from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

class User_info(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    role = models.CharField(max_length=30,null=True)
    description=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return "{}".format(self.role)


def create_user_info(sender, instance, created, **kwargs):
    if created:
        User_info.objects.create(user=instance)

post_save.connect(create_user_info, sender=User)

booked_by=(("nss","NSS"),
            ("voyagers","Voyagers"),
            ("saasc","SAASC"),("CSS","CSS"),("IEEE","IEEE"),
            ("robotics","robotics"),
            ("music_club","music_club"))
req_venue=(
    ("l26","LH-26"),("l27","LH-27"),("l28","LH-28"),
    ("Auditorium","Auditorium"),
    ("Audi With Arena","Audi Arena")
    )
lab_venue=(("Lab-303","lab-303"),
            ("Lab-306","lab-306"),
            ("Lab-307","lab-307"),
            ("CL-13","CL-13"),
            ("CL-14","CL-14")
            )


class venue(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    rew_by_oi= models.BooleanField(default=False)
    rew_by_hod= models.BooleanField(default=False)
    rew_by_labt= models.BooleanField(default=False)
    app_by_cdgc= models.BooleanField(default=False)
    app_by_ois= models.BooleanField(default=False)
    app_by_da= models.BooleanField(default=False)
    app_by_dsa= models.BooleanField(default=False)
    app_final= models.BooleanField(default=False)
    considered= models.BooleanField(default=False)
    date=models.DateField()

    requested_venue_secy= models.CharField(max_length=20,choices=req_venue,null=True,blank=True)
    requested_venue_student= models.CharField(max_length=20,choices=lab_venue,null=True,blank=True)
    event_name= models.CharField(max_length=300,null=True)
    associated_club=models.CharField(max_length=20,choices=booked_by,null=True,blank=True)

    def __str__(self):
        if self.requested_venue_secy:
            return self.requested_venue_secy
        elif self.requested_venue_student:
            return self.requested_venue_student
