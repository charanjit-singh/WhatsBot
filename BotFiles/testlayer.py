__author__ = 'Charanjit'
import os
from yowsup.layers.protocol_media.mediadownloader import MediaDownloader
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import psycopg2
import csv
from yowsup.layers.protocol_profiles.protocolentities import SetStatusIqProtocolEntity
from yowsup.layers.protocol_contacts.protocolentities import GetSyncIqProtocolEntity, ResultSyncIqProtocolEntity
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_chatstate.protocolentities import ChatstateProtocolEntity, OutgoingChatstateProtocolEntity
from yowsup.layers.protocol_chatstate import YowChatstateProtocolLayer
from yowsup.layers.protocol_presence.protocolentities.presence_available import AvailablePresenceProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
from yowsup.layers.protocol_presence.protocolentities.presence_unavailable import UnavailablePresenceProtocolEntity
from yowsup.common.tools import Jid
import shutil
from yowsup.layers.protocol_media.mediadownloader import MediaDownloader
from yowsup.layers.auth import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
import random
import time
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers import YowLayerEvent, EventCallback
from yowsup.layers.network import YowNetworkLayer
import sys
from yowsup.common import YowConstants
from datetime import datetime
import os
import logging
from yowsup.layers.protocol_groups.protocolentities      import *
from yowsup.layers.protocol_presence.protocolentities    import *
from yowsup.layers.protocol_messages.protocolentities    import *
from yowsup.layers.protocol_ib.protocolentities          import *
from yowsup.layers.protocol_iq.protocolentities          import *
from yowsup.layers.protocol_contacts.protocolentities    import *
from yowsup.layers.protocol_chatstate.protocolentities   import *
from yowsup.layers.protocol_privacy.protocolentities     import *
from yowsup.layers.protocol_media.protocolentities       import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_profiles.protocolentities    import *
from yowsup.common.tools import Jid
from yowsup.common.optionalmodules import PILOptionalModule, AxolotlOptionalModule
import threading

forwarding=False
lockXact=False
list_cont=['919417290392','917508377911']
downloading=0
list_link='Not specified'
DB_CONNECTION = None

class Whatsbot(YowInterfaceLayer):
    PROP_RECEIPT_AUTO       = "org.openwhatsapp.yowsup.prop.cli.autoreceipt"
    PROP_RECEIPT_KEEPALIVE  = "org.openwhatsapp.yowsup.prop.cli.keepalive"
    PROP_CONTACT_JID        = "org.openwhatsapp.yowsup.prop.cli.contact.jid"
    EVENT_LOGIN             = "org.openwhatsapp.yowsup.event.cli.login"
    EVENT_START             = "org.openwhatsapp.yowsup.event.cli.start"

    def onEvent(self, event):
        if event.getName()== 'Whatsbot_Phone':
            self.BotPhoneNumber = str(event.getArg('phone_num'))
            # print (self.BotPhoneNumber)

            return True      # Not to BROADCAST Further
        if event.getName() == 'Continue_Sending':
            print('Continue sending')
            self.spamMessages()
            return True



    def __init__(self):
        self.BotPhoneNumber = '917009213133'
        super(Whatsbot,self).__init__()
        YowInterfaceLayer.__init__(self)
        self.GOT_CONTACTS = False
        self.csvlink = ''
        self.SYNC_CONTACTS = [] #List of contacts which need to be synced
        self.LIST_CONTACTS = [] # List of Contacts to whom mwssage has to be sent
        print('Layer Running')
        global DB_CONNECTION
        getDbConnection()
        self.connection = DB_CONNECTION
        self.forwarding = False
        self.lockXact=False
        self.ackQueue = []
        self.lock = threading.Condition()







    @ProtocolEntityCallback("notification")
    def onNotification(self, notification):
        print('New Notification')
        self.toLower(notification.ack())

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        global got_list
        self.online()
        self.make_presence()
        time.sleep(random.uniform(0.5,1.0))
        self.toLower(messageProtocolEntity.ack(True))    # // Sending Double tick
        time.sleep(random.uniform(0.5,1.0))
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(),
                                                        'read', messageProtocolEntity.getParticipant())
        self.toLower(receipt)
        time.sleep(random.uniform(0.5,1.0))
        self.start_typing(messageProtocolEntity.getFrom())
        #time.sleep(10)
        # global lockXact
        # global forwarding
        time.sleep(random.uniform(0.5,1.0))
        self.stop_typing(messageProtocolEntity.getFrom())
        print(messageProtocolEntity.getType()+" Message from "+messageProtocolEntity.getFrom())
        # self.sendMessage(messageProtocolEntity.getFrom(),str(self.BotPhoneNumber))
        if(self.senderIsAdmin(messageProtocolEntity.getFrom())):
            print("Admin Sent a message")
            if messageProtocolEntity.getType()=='text':
                if (not self.iscmd(messageProtocolEntity.getBody())) and self.forwarding == True:
                    if True:
                        self.lockXact=True
                        message_backup = messageProtocolEntity.getBody()
                        if DB_CONNECTION == None:
                            getDbConnection()
                        cur = DB_CONNECTION.cursor()
                        cur.execute('Select admin_id_id from public.wbot_adminbot where bot_id_id in (select id from public.wbot_bot where bot_phone = \'%s\')'  %str(self.BotPhoneNumber))
                        admin_id = str(cur.fetchone()[0])
                        cur.execute('select id from public.wbot_bot where bot_phone = \'%s\'' %str(self.BotPhoneNumber))
                        bot_id = str(cur.fetchone()[0])
                        cur.execute('select docfile from public.wbot_document where auto_pseudoid = \'%s\';' %self.csvlink)
                        file_path = cur.fetchone()[0]
                        file_path = '/media/'+file_path
                        cur.execute('Insert Into public.wbot_message(message_text,admin_id,"csvFile","startedOn") values (\'%s\',\'%s\',\'%s\',TIMESTAMP \'%s\') returning id;' %(message_backup,admin_id,file_path,datetime.now()))
                        message_id = str(cur.fetchone()[0])
                        print('Storing Contacts into Data base')
                        for phone_number in self.LIST_CONTACTS:

                            print(self.LIST_CONTACTS)
                            ph_no = phone_number
                            # phone_number = validate(phone_number[0])
                            print(phone_number)
                            cur.execute('Insert into public.wbot_messagestatus(phon_num,status,bot_id_id,message_id_id) values (\'%s\',\'0\',\'%s\',\'%s\')' %(ph_no,bot_id,message_id))
                            print('Written ',phone_number,' on Database')
                        DB_CONNECTION.commit()
                        cur.close()

                        # # global list_cont
                        # print("Started Sending")
                        # message_to_send = messageProtocolEntity.getBody()
                        # # backup message_to_send content to Database
                        # for num in list_cont:
                        #     if len(num)<12:
                        #         num='91'+num
                        #         if len(num)<12:
                        #             continue
                        #     if len(num)>12:
                        #         num=num[-12:]
                        #     self.forwardMessage(messageProtocolEntity,num)
                        #    print("Message Sent to "+num)
                        # put n database the message sent
                        # self.lockXact=False
                        print("lockXact Released on sending")
                        self.spamMessages()

                    else:
                        self.sendError(messageProtocolEntity.getFrom(),'busy')
                        #WhatsBot Busy
                elif self.iscmd(messageProtocolEntity.getBody()):
                    statement=messageProtocolEntity.getBody()
                    pookle=statement.split(' ') # pookle stands for segment
                    try:
                        command=pookle[1].lower()
                    except IndexError:
                        command='Wrong_Command_Sent'
                    if command=="start":
                        #getlist(messageProtocolEntity.getBody())

                        if self.GOT_CONTACTS==True:
                            self.forwarding=True;
                            #warn client
                        else:
                            self.sendError(messageProtocolEntity.getFrom(),'list_not_specified')
                            # List not specified Error
                    elif command=="stop":
                        if self.forwarding==True:
                            print('Stopped Forwarding')
                            self.forwarding=False
                        elif self.forwarding==False:
                            self.sendError(messageProtocolEntity.getFrom(),'already_stopped')
                            #Error Wasn't Sending Already stopped
                    elif command=="list":
                        self.setlist(self.fetchlink(messageProtocolEntity.getBody()))
                    elif command=='help':
                        self.showhelp(messageProtocolEntity.getFrom())
                    elif command=='offers':
                        self.showoffers(messageProtocolEntity.getFrom())
                    elif command=='status':
                        print("Show STATE")

                        self.profile_setStatus()
                        self.profile_setPicture('/home/charanjit/project_whatsbot/BotFiles/wa.jpg')
                        #self.sendStats(messageProtocolEntity.getFrom())
                    elif command == 'image':
                        self.image_send(messageProtocolEntity.getFrom(),'/home/charanjit/project_whatsbot/BotFiles/wa.jpg')
                else:
                    self.sendError(messageProtocolEntity.getFrom(),'incorrect_command')
            else:

                print('Handle Media Messages')

                self.showHelp_S(messageProtocolEntity.getFrom(),messageProtocolEntity.getNotify())
                #self.onMediaMessage(messageProtocolEntity)
                #Handle media message
        else:
            if not  messageProtocolEntity.isGroupMessage():
                self.showHelp_S(messageProtocolEntity.getFrom(),messageProtocolEntity.getNotify())
                print('Show Help to strangers')
            else:
                print("was a group message")

#show help to strangers




    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        type_reciept= entity.getType()
        if(type_reciept=='read'):
            if DB_CONNECTION ==None:
                getDbConnection()
            cur  = DB_CONNECTION.cursor()
            cur.execute('update public.wbot_messagestatus set status  = \'2\' where phon_num = \'%s\''%entity.getFrom()[0:12])
            print(entity.getFrom()[0:12]+' Read the messages ')
            DB_CONNECTION.commit()

            # def onReceipt(self, entity):
        self.toLower(entity.ack())


        # self.toLower(entity.ack())



    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        print('Connection Success With Whatsapp Server')
        self.online()
        self.make_presence()
        self.spamMessages()


    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()
        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))
        self.lock.release()


    def onMediaMessage(self, messageProtocolEntity):
         if messageProtocolEntity.getMediaType() == "image":
            self.tmpto = messageProtocolEntity.getFrom()
            data = messageProtocolEntity.getMediaContent()
            outPath = os.path.join("mm.jpg" )
            print(outPath)
            f = open(outPath, 'wb')
            f.write(data)
            f.close()
            self.onsuccess(outPath)

    def onError(self):
        self.toLower(TextMessageProtocolEntity("Foto konnte nicht gespeichert werden", to = self.tmpto))

    def onsuccess(self, path):
        self.toLower(TextMessageProtocolEntity("Foto gespeichert (%s)" % (os.path.basename(path)), to = self.tmpto))

    def onProgress(self, progress):
        pass

    def doSendMedia(self, mediaType, filePath, url, to, ip = None, caption = None):
        if mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE:
        	entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
        	entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to)
        elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO:
        	entity = VideoDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        self.toLower(entity)

    # @clicmd("Send a video with optional caption")
    def video_send(self, number, path, caption = None):
        self.media_send(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO)

    # @clicmd("Send an image with optional caption")
    def image_send(self, number, path, caption = None):
        self.media_send(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE)

    # @clicmd("Send audio file")
    def audio_send(self, number, path):
        self.media_send(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO)

    def media_send(self, number, path, mediaType, caption = None):
        if True:
            jid = (number)
            entity = RequestUploadIqProtocolEntity(mediaType, filePath=path)
            successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, mediaType, path, successEntity, originalEntity, caption)
            errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)
            self._sendIq(entity, successFn, errorFn)

            self._sendIq(entity, successFn, errorFn)
    ## Callbacks
    def onRequestUploadResult(self, jid, mediaType, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, caption = None):
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendMedia(mediaType, filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                             resultRequestUploadIqProtocolEntity.getIp(), caption)
        else:
            successFn = lambda filePath, jid, url: self.doSendMedia(mediaType, filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      successFn, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()
    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        print("Request upload for file %s for %s failed" % (path, jid))

    def onUploadError(self, filePath, jid, url):
        print("Upload file %s to %s for %s failed!" % (filePath, url, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        sys.stdout.flush()



    def profile_setPicture(self, path):
        if True:
            with PILOptionalModule(failMessage = "No PIL library installed, try install pillow") as imp:
                Image = imp("Image")
                def onSuccess(resultIqEntity, originalIqEntity):
                    print("Profile picture updated successfully")

                def onError(errorIqEntity, originalIqEntity):
                    lprint("Error updating profile picture")

                #example by @aesedepece in https://github.com/tgalal/yowsup/pull/781
                #modified to supportsrc python3
                src = Image.open(path)
                pictureData = src.resize((640, 640)).tobytes("jpeg", "RGB")
                picturePreview = src.resize((96, 96)).tobytes("jpeg", "RGB")
                iq = SetPictureIqProtocolEntity(self.getOwnJid(), picturePreview, pictureData)
                self._sendIq(iq, onSuccess, onError)


    def spamMessages(self):
        print('Spamming Messages')
        if DB_CONNECTION == None:
            getDbConnection()
            print('Got Database Connection')
        print(DB_CONNECTION)
        cur = DB_CONNECTION.cursor()
        # while True:

        cur.execute('Select admin_id_id from public.wbot_adminbot where bot_id_id in (select id from public.wbot_bot where bot_phone = \'%s\')' %str(self.BotPhoneNumber))
        admin_id = str(cur.fetchone()[0])
        print('Admin Id :' ,admin_id)
        cur.execute('Select id,message_text from public.wbot_message where admin_id  = \'%s\' and id in(select message_id_id from public.wbot_messagestatus where status = \'0\')' %admin_id )
        message_id_list = (cur.fetchall())
        # TODO: loop until not every message is sent
        print(message_id_list)
        i=0
        for message_ids in message_id_list:
            print(message_ids)
            message_id= str(message_ids[0])
            message_text = str(message_ids[1])
            print('Message Id: ',message_id)
            print('Message Text: ',message_text)
            cur.execute('select id from public.wbot_bot where bot_phone = \'%s\' and bot_state =\'2\'' %self.BotPhoneNumber )
            bot_id = str(cur.fetchone()[0])
            print('Bot Id: ',bot_id)
            cur.execute('select phon_num from public.wbot_messagestatus where message_id_id = \'%s\' and  status = \'0\' '%message_id )
            phone_nums = cur.fetchall()
            print('Phone number List: ',phone_nums)
            #TODO:Sync Contacts Here
            #   Get Already contacts synced List
            #   Get New Contact LIST
            #   if all(New Contact List ) in Already Contact Synced list:
            #       then do nothing
            #   else
            #       get those contacts that are not in Already Synced List but in New contact list
            #       append them to Already  Synced List
            #       contacts_sync(Already contact list)
            #     def contacts_sync(self, contacts):
            #        entity = GetSyncIqProtocolEntity(contacts)
            #        print (syncing)
            #         self.toLower(entity)
            # print(phone_nums)
            for phone_number in phone_nums:

                phone_number = phone_number[0]
                ph_num = phone_number
                self.LIST_CONTACTS.append(ph_num)

            self.OptimiseList()

            syncEntity = GetSyncIqProtocolEntity(self.LIST_CONTACTS)
            self.toLower(syncEntity)

            self.lock.acquire()
            print('Lock acquired on Thread')
            for phone_number in phone_nums:
                try:
                    phone_number = phone_number[0]
                    print('Phone number: ',phone_number)
                    ph_num = phone_number
                    phone_number = phone_number+'@s.whatsapp.net'
                    self.sendMessage(phone_number,message_text)
                    # print('update public.wbot_messagestatus set status = \'1\' where phon_num = \'%s\' and message_id_id = \'%s\'' %(ph_num, message_id))
                    cur.execute('update public.wbot_messagestatus set status = \'1\' where phon_num = \'%s\' and message_id_id = \'%s\'' %(ph_num, message_id))
                    DB_CONNECTION.commit()
                except AuthError:
                    cur.close()
                    DB_CONNECTION.close()
                    raise AuthError()
                i = i+1
            self.lock.release()

        cur.close()




    def forwardMessage(self,outgoingMessageProtocolEntity,num):
        num=num+'@s.whatsapp.net'
        self.start_typing(num)
        time.sleep(random.uniform(0.5,1.0))
        entity=outgoingMessageProtocolEntity.forward(num)
        self.toLower(entity)
        self.stop_typing(num)
        time.sleep(random.uniform(0.6,1.0))
        self.start_typing(num)
        time.sleep(random.uniform(0.6,0.5))
        self.stop_typing(num)
        time.sleep(random.uniform(0.6,0.9))
        #self.disconnect()
    def fetchlink(self,message):
        try:
            _url=message.split(' ')
            url=_url[2]
        except:
            url='error'

        print (url)
        return url

    def sendMessage(self,num,message):
        # num=num+'@s.whatsapp.net'
        num =self.normalise(num)
        self.start_typing(num)
        time.sleep(random.uniform(0.1,0.3))
        messageEntity= TextMessageProtocolEntity(
            message,
            to=num)
        self.ackQueue.append(messageEntity.getId())
        self.toLower(messageEntity)
        # self.toLower(entity)
        # print('Message: ',message,' To: ',num)
        self.stop_typing(num)
        time.sleep(random.uniform(0.1,0.3))
        self.start_typing(num)
        time.sleep(0.1)
        self.stop_typing(num)
        # time.sleep(random.uniform(0.5,1.0))




    def setlist(self,link):
        if link=='error':
            print('List Error . . . .. .')
            return
        if getList(link):
            self.csvlink = link
            self.LIST_CONTACTS = []
            if DB_CONNECTION ==None:
                getDbConnection()
            cur = DB_CONNECTION.cursor()
            cur.execute('select docfile from public.wbot_document where auto_pseudoid = \'%s\';' %link)
            try:
                file_path = cur.fetchone()[0]
                file_path = '../media/'+file_path
            except:
                self.sendError(messageProtocolEntity.getFrom(),'incorrect_command')
                return
            import pandas as pd
            valid = True
            csv_file = open(file_path)
            df = pd.read_csv(csv_file)
            try:
                saved_column = df['phone']
            except KeyError:
                try:
                    saved_column = df['contacts']
                except KeyError:
                    try:
                        saved_column = df['contact']
                    except KeyError:
                        try:
                            saved_column =df['numbers']
                        except KeyError:
                            try:
                                saved_column = df['number']
                            except KeyError:
                                print('Error CSV')
                                valid = False
                                self.GOT_CONTACTS = False

            if valid:
                print(saved_column)
                for contact in saved_column:
                    contact = str(contact)
                    contact.replace('-','')
                    contact.replace('+','')
                    if len(contact)==10:
                        contact = '91'+contact
                    elif len(contact) > 10:
                        contact = contact[-10:]
                        contact = '91'+ contact

                    self.LIST_CONTACTS.append(contact)
                self.GOT_CONTACTS = True
        else:
            self.GOT_CONTACTS = False

        #
        # global list_cont
        # global downloading
        # if downloading==0:
        #     try:
        #         self.download_file(link)
        #
        #
        #         csv_file = open('contacts.csv') # path of the csv file
        #         reader = csv.reader(csv_file)
        #
        #         for line in reader:
        #             list_of_headers = [header for header in line]
        #             phone_index = list_of_headers.index('phone')
        #             break
        #
        #         list_cont = [line[phone_index] for line in reader]
        #         print(list_cont)
        #         got_list=True
        #     except:
        #         got_list=False
        #         #Failure



        # else:
        #     print ("Already Downloading")


    def download_file(self,initialurl):

        import requests
        global downloading
        downloading=0
        from html.parser import HTMLParser
        result = requests.get(initialurl)
        if result.status_code==200:
            c = result.content
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(c, 'html.parser')
            link = soup.find_all("a", "btn btn-default hvr-shrink downloadButton")
            link=str(link)
            links=link.find('href')
            print(links)
            print(link.find('/">'))
            mm=link.split('=')
            mm=str(mm[2])
            mm=mm.split('"')
            url='https://nofile.io'+mm[1]
            import shutil
            response = requests.get(url, stream=True)
            if response.status_code==200:
                downloading=1
                with open('contacts.csv', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
                downloading=0
            else:
                print('Error in url')
        else:
            print('Error in url')




    def make_presence(self):
        self.toLower(PresenceProtocolEntity(name="WhatsBot"))


    def online(self):
        self.toLower(AvailablePresenceProtocolEntity())

    def disconnect(self):
        self.toLower(UnavailablePresenceProtocolEntity())

    def start_typing(self,from_):
        self.toLower(OutgoingChatstateProtocolEntity(
            OutgoingChatstateProtocolEntity.STATE_TYPING,
            from_
        ))
    def stop_typing(self,num):
        self.toLower(OutgoingChatstateProtocolEntity(
            OutgoingChatstateProtocolEntity.STATE_PAUSED,
            num
        ))

    def sendError(self,num,param):
        message=''
        if param=='already_stopped':
            message='💬 *Info:*\nMessage sending has been stopped already.😅'
        elif param=='incorrect_command':
            message='❗ *Error:* \nSorry, I can\'t recognise such type of commands.😢\n send *WB help* for help.😄'
        elif param=='list_not_specified':
            message='❗ *Error:* \nList not specified👎.send *WB help* for help.🛃'
        elif param=='busy':

            message='❗ *Error:* \nCan you please hold on!.😕 I\'m busy right now.🤕'
        else:
            message='⁉ *Error:* \nError not found.😰😰'

        self.sendMessage(num,message)


    def iscmd(self,param):
        pookle=param.split(' ')
        if(pookle[0].lower()=='whatsbot' or pookle[0].lower()=='wb' ):
            return  True
        else:
            return False

    def senderIsAdmin(self,contact):
        if '919996009129@s.whatsapp.net'==contact or '919417290392@s.whatsapp.net'==contact or '918950844543@s.whatsapp.net'==contact:
            return True
        return False

    def normalise(self,jid):
        try:
            jid.find('@s.whatsapp')
            return jid
        except ValueError:
            return jid+'@s.whatsapp.net'
    def showhelp(self,num):
        message='*WhatsBot*🤖 \nCommands avilable:\n\n👉🏻 *WB help* for showing this message.\n👉🏻 Step 1: Upload contacts list at https://nofile.io (csv format only)\n👉🏻 Step 2: *WB list* <paste nofile.io link here>.\n *Phone numbers must be uploaded on https://nofile.io .*\n👉🏻 Step 3: *WB Start* Sends messages to list specified after this command.\n👉🏻 Step 4: *TYPE THE MESSAGE YOU WANT TO BROADCAST*\n 👉🏻 Step 5: *WB Stop* Stops sending messages after this command to list.\n\n\n🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖'
        self.sendMessage(num,message)
    def showoffers(self,num):
        message='Showing offers'
        self.sendMessage(num,message)
    def showHelp_S(self,num,name):
        #message="*Hello "+name+" .*\nI'm WhatsBot.🤖\nI was born on 10 Dec,2017😀.\nMy Father is Charanjit Singh.👪\nI have capability🤓 to:\n👉🏻Send bulk messages🗯 to single contact.\n👉🏻Send messages to a list of contacts.\n👉🏻Show current Status.My Dad told me that I'll be supporting Web interface and Group sending support soon😁. I'm so excited 😁😁.Can't Wait for it.😍😄"
        # message="Thanks for messaging *AAABrightAcademy.* \nYou can visit our website aaabrightacademy.in for knowing about the various coaching courses we offer at our different centers in North India and you may also call us at: +91-98724-74753 for any details!\n\nBest Regards,\nTeam AAABrightAcademy,"
         #   num.find('@g.us')
        #    print('Was Group Message'
        #except  ValueError:
        message = 'Thank you '+ name + ' for messaging us.'
        self.sendMessage(num,message)


    def getcontext():
        return self

    def profile_setStatus(self):
        text = 'Hey there! I am WhatsBot .'
        def onSuccess(resultIqEntity, originalIqEntity):
            print("Status updated successfully")

        def onError(errorIqEntity, originalIqEntity):
            print("Error updating status")

        entity = SetStatusIqProtocolEntity(text)
        self._sendIq(entity, onSuccess, onError)





    def OptimiseList(self):
        tempList = []
        for tpl in self.LIST_CONTACTS:

            tempList.append(str(tpl))

        self.LIST_CONTACTS = tempList
        print('Optimised List: ',self.LIST_CONTACTS)




def getDbConnection():
    global DB_CONNECTION

    while True:
        try:
            print('Trying To get DB Connection')
            DB_CONNECTION = psycopg2.connect(host = 'localhost' , user = 'postgres' ,password = 'root' ,database = 'whatsbot')
        except DatabaseError:
            DB_CONNECTION = None
            continue
            print('DB connection Error in WhatsBot Layer')
        if DB_CONNECTION == None:
            continue
        else :
            break

def getList(url):
    # Download CSV and Store into Database
    return True
