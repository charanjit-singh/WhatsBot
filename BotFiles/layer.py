__author__ = 'Charanjit'

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_chatstate.protocolentities import ChatstateProtocolEntity, OutgoingChatstateProtocolEntity
from yowsup.layers.protocol_chatstate import YowChatstateProtocolLayer
import time
send_next=0
class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        is_admin = 0
        global send_next
        send_next_=send_next
        admin_number='919417290392@s.whatsapp.net'
        message='Whatsbot'
        Demo_Message="*WhatsBot*: \nSend Whatsapp messages by chatting with our WhatsBot."
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(),
                                                        'read', messageProtocolEntity.getParticipant())
        time.sleep(0.5)
        self.toLower(receipt)
        print("Message from "+messageProtocolEntity.getFrom())
        if(messageProtocolEntity.getFrom()==(admin_number)):
            print("IS admin number")
            if send_next_==1:
                list_cont={'919417290392','917508377911'}
                if messageProtocolEntity.getType()=='text':
                    try:
                        if ( (messageProtocolEntity.getBody()).index('WhatsBot --end') ==0):
                            send_next=0
                            print("Sending Disabled")
                        else:
                            print("Sending Message")
                    except:
                        for contact_member in list_cont:
                            entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_TYPING, contact_member+'@s.whatsapp.net')
                            self.toLower(entity)
                            self.toLower(messageProtocolEntity.forward(contact_member+'@s.whatsapp.net'))
                            print ("Sending to :", contact_member)
                        
                else:
                    print("Is media")
                    #for contact_member in list_cont:
                        #self.toLower(messageProtocolEntity.forward(contact_member+'@s.whatsapp.net'))
                        #print ("Sending to :", contact_member)

                    
            if messageProtocolEntity.getType()=='text':
                print("Is Text")
                message=messageProtocolEntity.getBody()
                try:
                    if((messageProtocolEntity.getBody()).index('WhatsBot --send')==0):
                        send_next=1
                        print("Send Next ")
                except:
                    print("Message Passed")

        else:
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                Demo_Message,
                to=messageProtocolEntity.getFrom())
            self.toLower(outgoingMessageProtocolEntity)
            
            
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())
    
    
    
    
    
    def download_file(self,initialurl):
        #btn btn-default hvr-shrink downloadButton
        import requests
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
                with open('python.py', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
            else:
                print('Error in url')
        else:
            print('Error in url')
