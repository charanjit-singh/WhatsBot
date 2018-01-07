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

class Detect(YowInterfaceLayer):
    
    PROP_RECEIPT_AUTO       = "org.openwhatsapp.yowsup.prop.cli.autoreceipt"
    PROP_RECEIPT_KEEPALIVE  = "org.openwhatsapp.yowsup.prop.cli.keepalive"
    PROP_CONTACT_JID        = "org.openwhatsapp.yowsup.prop.cli.contact.jid"
    EVENT_LOGIN             = "org.openwhatsapp.yowsup.event.cli.login"
    EVENT_START             = "org.openwhatsapp.yowsup.event.cli.start"

    def __init__(self):
        super(Detect,self).__init__()
        YowInterfaceLayer.__init__(self)
        print('Layer Running')
        self.LIST_CONTACTS=[]
        self.GOT_CONTACTS=False
        self.myfile=None
        self.wr=None
        

    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        print('Connection Success With Whatsapp Server')
        self.presence_name('Isha Testing')
        self.presence_available()
        self.setlist('34CAB5B')
        self.myfile = open('filtered.csv', 'w') 
        self.wr = csv.writer(self.myfile, quoting=csv.QUOTE_ALL)
        self.wr.writerow(['phone','last'])
        self.scanList()

    
    @ProtocolEntityCallback('presence')
    def onPresence(self,data):
        print('Presence:--------------')
        number=data.getFrom(full=False)
        lastState=data.getLast()
        if lastState is not None:
            print('[',number,']','---','[',lastState,']')
            contactStateList= [number,lastState]
            self.wr.writerow(contactStateList)
            
            self.presence_unsubscribe(number)
            self.myfile.flush()

    

        
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print(entity)
        self.toLower(entity.ack())


    @ProtocolEntityCallback("chatstate")
    def onChatstate(self, entity):
        print(entity)
        
        
            
    def presence_name(self, name):
        if self.assertConnected():
            entity = PresenceProtocolEntity(name = name)
            self.toLower(entity)



    def presence_available(self):
        if self.assertConnected():
            entity = AvailablePresenceProtocolEntity()
            self.toLower(entity)
            

    def presence_subscribe(self, contact):
        if self.assertConnected():
            entity = SubscribePresenceProtocolEntity((contact)+'@s.whatsapp.net')
            self.toLower(entity)


    def presence_unsubscribe(self, contact):
        if self.assertConnected():
            entity = UnsubscribePresenceProtocolEntity((contact)+'@s.whatsapp.net')
            self.toLower(entity)

            
            
    def assertConnected(self):
        return True
       
###############################################################################################################################

    def scanList(self):
        self.OptimiseList()
        syncEntity = GetSyncIqProtocolEntity(self.LIST_CONTACTS)
        print('Syncing')
        self.toLower(syncEntity)
        i=0
        # get all numbers from Database and scan them
        # subscribe in 100 -100 batches
        for contacts in self.LIST_CONTACTS:
            self.presence_subscribe(contacts)
            i=i+1
            print(i)
        print('done')
        i=0
        self.presence_subscribe('919463472922')
        self.presence_subscribe('919417290392')
        self.presence_subscribe('917589244662')
        
    
        
        
################################################################################################################################

    def OptimiseList(self):
        tempList = []
        for tpl in self.LIST_CONTACTS:

            tempList.append(str(tpl))

        self.LIST_CONTACTS = tempList

    def setlist(self,link):
        if link=='error':
            print('List Error . . . .. .')
            return
        if True:
            self.LIST_CONTACTS = []
            if DB_CONNECTION ==None:
                getDbConnection()
            cur = DB_CONNECTION.cursor()
            cur.execute('select docfile from public.wbot_document where auto_pseudoid = \'%s\';' %link)
            try:
                file_path = cur.fetchone()[0]
                file_path = '../../media/'+file_path
            except:
                #self.sendError(self.phone_num_last,'incorrect_file')
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
                                self.sendError(self.phone_num_last,'incorrect_file')
                                valid = False
                                self.GOT_CONTACTS = False

            if valid:
                print(saved_column)
                for contact in saved_column:
                    contact = str(contact)
                    contact.replace('-','')
                    contact.replace('+','')
                    contact.replace('.0','')
                    if len(contact)<10:
                        contact='9417290392'
                    if len(contact)==10:
                        contact = '91'+contact
                    elif len(contact) > 10:
                        contact = contact[-10:]
                        contact = '91'+ contact

                    self.LIST_CONTACTS.append(contact)
                self.GOT_CONTACTS = True
        else:
            self.GOT_CONTACTS = False







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

################################################################################################################################
