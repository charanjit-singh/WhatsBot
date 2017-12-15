__author__ = 'Charanjit'

import csv
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_chatstate.protocolentities import ChatstateProtocolEntity, OutgoingChatstateProtocolEntity
from yowsup.layers.protocol_chatstate import YowChatstateProtocolLayer
from yowsup.layers.protocol_presence.protocolentities.presence_available import AvailablePresenceProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
from yowsup.layers.protocol_presence.protocolentities.presence_unavailable import UnavailablePresenceProtocolEntity
import random
import time
forwarding=False
lock=False
list_cont=['919417290392']
downloading=0
got_list=False
list_link='Not specified'
current_progress=0
class Whatsbot(YowInterfaceLayer):


    current_bot='0000000000'
    @ProtocolEntityCallback("notification")
    def onNotification(self, notification):
        print('New Notification')
        self.toLower(notification.ack())

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        global got_list
        self.online()
        self.make_presence()
        time.sleep(random.uniform(1,2))
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(),
                                                        'read', messageProtocolEntity.getParticipant())
        self.toLower(receipt)
        time.sleep(random.uniform(0.5,2.0))
        self.start_typing(messageProtocolEntity.getFrom())
        #time.sleep(10)
        global lock
        global forwarding
        time.sleep(random.uniform(0.5,2.0))
        self.stop_typing(messageProtocolEntity.getFrom())
        print(messageProtocolEntity.getType()+" Message from "+messageProtocolEntity.getFrom())
        if(self.senderIsAdmin(messageProtocolEntity.getFrom())):
            print("Admin Sent a message")
            if messageProtocolEntity.getType()=='text':
                if (not self.iscmd(messageProtocolEntity.getBody())) and forwarding == True:
                    if lock== False:
                        lock=True
                        global list_cont
                        print("Started Sending")
                        for num in list_cont:
                            if len(num)<12:
                                num='91'+num
                                if len(num)<12:
                                    continue
                            if len(num)>12:
                                num=num[-12:]

                            self.forwardMessage(messageProtocolEntity,num)
                            print("Message Sent to "+num)
                        lock=False
                        print("Lock Released on sending")

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
                        got_list=True
                        if got_list==True:
                            forwarding=True;
                            #warn client
                        else:
                            self.sendError(messageProtocolEntity.getFrom(),'list_not_specified')
                            # List not specified Error
                    elif command=="stop":
                        if forwarding==True:
                            print('Stopped Forwarding')
                            forwarding=False
                        elif forwarding==False:
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
                        #self.sendStats(messageProtocolEntity.getFrom())

                else:
                    self.sendError(messageProtocolEntity.getFrom(),'incorrect_command')
            else:

                print('Handle Media Messages')
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
        self.toLower(entity.ack())


    def forwardMessage(self,outgoingMessageProtocolEntity,num):
        num=num+'@s.whatsapp.net'
        self.start_typing(num)
        time.sleep(random.uniform(0.5,1.5))
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
        num=self.normalise(num)
        self.start_typing(num)
        time.sleep(random.uniform(1.1,2.0))
        entity= TextMessageProtocolEntity(
            message,
            to=num)
        self.toLower(entity)
        self.stop_typing(num)
        time.sleep(random.uniform(0.3,1.9))
        self.start_typing(num)
        time.sleep(random.uniform(0.5,0.6))
        self.stop_typing(num)
        time.sleep(random.uniform(0.5,1.5))



    def setlist(self,link):
        if link=='error':
            print('List Error . . . .. .')
            return
        global list_cont
        global downloading
        if downloading==0:
            try:
                self.download_file(link)


                csv_file = open('contacts.csv') # path of the csv file
                reader = csv.reader(csv_file)

                for line in reader:
                    list_of_headers = [header for header in line]
                    phone_index = list_of_headers.index('phone')
                    break

                list_cont = [line[phone_index] for line in reader]
                print(list_cont)
                got_list=True
            except:
                got_list=False
                #Failure



        else:
            print ("Already Downloading")


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
        message="Thanks for messaging *AAABrightAcademy.* \nYou can visit our website aaabrightacademy.in for knowing about the various coaching courses we offer at our different centers in North India and you may also call us at: +91-98724-74753 for any details!\n\nBest Regards,\nTeam AAABrightAcademy,"
         #   num.find('@g.us')
        #    print('Was Group Message'
        #except  ValueError:
        self.sendMessage(num,message)


    def getcontext():
        return self
