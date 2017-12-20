from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import IntegrityError
import random
# this file contains Database models needed for WhatsBot v1.0
class Admin(models.Model):
    # admin_id =  models.AutoField(primary_key=True)
    admin_phone = models.CharField(max_length=13)
    authUser = models.OneToOneField(User)
    # def add_admin(self,phone,password):
    #     self.admin_phone=phone
    #     self.admin_login=password

# Bots Model

class Bot(models.Model):
    # bot_id = models.AutoField(primary_key=True)
    bot_phone = models.CharField(max_length=13)
    bot_otp = models.CharField(max_length=7)
    bot_pwd = models.CharField(max_length=60)
    bot_state = models.IntegerField(default= 0)
    # 0 = Active, 1  = Blocked

# Admin is  Owner of Bot #
class AdminBot(models.Model):
    admin_id = models.ForeignKey(Admin)
    bot_id = models.ForeignKey(Bot)
    def __str__(self):
        return self.admin_id.admin_phone

# Contact List Model
# class contact_list(models.Model):
#     # list_id = models.AutoField(primary_key=True)
#     list_phone = models.CharField(max_length=13)


# Messages With Id and is Media Attribue
class Message(models.Model):
    # message_id = models.AutoField(primary_key=True)
    # isMedia = models.BooleanField(default=False)
    message_text = models.CharField(max_length=1000, blank = True, null = True)
    message_image = models.ImageField(blank = True, null = True)
    csvFile = models.CharField(max_length=1000)
    admin = models.ForeignKey(Admin)
    startedOn = models.DateTimeField(auto_now_add = True)
    # list_id = models.ForeignKey(contact_list)

# Model to store Link of Csv or Xlsx Files

# Sync Status
class SyncStatus(models.Model):
    bot_id = models.ForeignKey(Bot)
    mobileNum = models.CharField(max_length = 13)

#Sending Status
class MessageStatus(models.Model):
    message_id = models.ForeignKey(Message)
    bot_id = models.ForeignKey(Bot)
    phon_num = models.CharField(max_length = 13)
    status = models.IntegerField(default = 0 )
    #status 0 = To process ,1 = Processing , 2 = Sent, 3 = Read


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    auto_pseudoid = models.CharField(max_length=7, blank=True, editable=False, unique=True)
    # add index=True if you plan to look objects up by it
    # blank=True is so you can validate objects before saving - the save method will ensure that it gets a value

    # other fields as desired

    def save(self, *args, **kwargs):
        if not self.auto_pseudoid:
            self.auto_pseudoid = generate_random_alphanumeric(7)
            # using your function as above or anything else
        success = False
        failures = 0
        while not success:
            try:
                super(Document, self).save(*args, **kwargs)
            except IntegrityError:
                 failures += 1
                 if failures > 5: # or some other arbitrary cutoff point at which things are clearly wrong
                     raise
                 else:
                     # looks like a collision, try another random value
                     self.auto_pseudoid = generate_random_alphanumeric(7)
            else:
                 success = True
        print(self.auto_pseudoid)
# End of Models


def generate_random_alphanumeric(k):
    return ''.join(random.choice('0123456789ABCDEF') for i in range(k))
