from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
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
    csvFile = models.FileField()
    admin = models.ForeignKey(Admin)
    # list_id = models.ForeignKey(contact_list)

# Model to store Link of Csv or Xlsx Files
# class ListLinks(models.Model):
#     list_id = models.ForeignKey(contact_list,db_column = 'list_id')
#     list_link = models.FilePathField(path = '/home/WhatsBot/lists',recursive= True)


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

# End of Models
