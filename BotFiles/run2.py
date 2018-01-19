__author__ = 'charanjit'

from yowsup.stacks import  YowStackBuilder
from testlayer import Whatsbot
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST
from yowsup.env import YowsupEnv
from config import Config
import psycopg2
import subprocess
import time
def startBot(credentials):
    print (credentials)
    credential_Pass = YowLayerEvent('Whatsbot_Phone',phone_num=credentials[0])
    stackBuilder = YowStackBuilder()
    # y = YowsupConnectionManager()
    # y.setAutoPong(True)
    stack = stackBuilder \
        .pushDefaultLayers(True) \
        .push(Whatsbot) \
        .build()
    stack.setCredentials(credentials)
    stack.setProp(PROP_IDENTITY_AUTOTRUST, True)

    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal
    stack.broadcastEvent(credential_Pass)
    # stack.loop(timeout=0.5, count=2) # Let the taskloop run one time for 2 seconds. So as to Setup complete
    # # Now Send Event to Scan if any Numbers in list remaining Whom to send messages
    # time.sleep(0.5)
    # stack.broadcastEvent(YowLayerEvent('Continue_Sending'))
    stack.loop()
    #
    # try:
    #     stack.loop() #this is the program mainloop
    # except AuthError as e:
    #     subprocess.call( ["/usr/bin/php", "way2sms-api.php"] )  #sending Sms
    #     print("Got Blocked !!! ")
    # except:
    #     stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))
    #     subprocess.call(["python3","run2.py"])
    #     subprocess.call( ["/usr/bin/php", "way2sms-api.php"] )


def main():
    # label : start
    while True:
        try:

            BotCredentials = ()
            conn =None
            try:
                conn = psycopg2.connect(host = 'localhost' , user = 'postgres' ,password = 'root' ,database = 'whatsbot')
            except DatabaseError:
                print('DB connection Error')
                continue
                # Using Contninue to restart

            if conn is not  None:
                # now database has been successfully connected
                # : Fetch bot phon and Password from Database
                cur = conn.cursor()
                # get Count of not blocked  bots

                cur.execute('Select id,bot_phone,bot_pwd from public.wbot_bot where not bot_state = 1 order by  id asc')
                row = cur.fetchone()
                if row is None:
                    print('No bot available')
                    if conn is not None:
                        conn.close()
                    # no bot available
                    # call main() again or goto start
                    continue


                cur.execute('Select id,bot_phone,bot_pwd from public.wbot_bot where  bot_state = 2 order by  id asc')
                row = cur.fetchone()
                if row is not None:
                    BotPhone=str(row[1])
                    BotPassword = str(row[2])
                    BotId=str(row[0])
                else:
                    #no bot is running Set Bot with minimal count to Running
                    cur.execute('Select id,bot_phone,bot_pwd from public.wbot_bot where  bot_state = 0 order by  message_count asc')
                    row = cur.fetchone()
                    BotPhone=str(row[1])
                    BotPassword = str(row[2])
                    BotId=str(row[0])
                    cur.execute('update public.wbot_bot set bot_state = \'2\' where id = \'%s\''%(str(BotId)))
                    #set to running : Successfull

                BotCredentials  = (BotPhone,BotPassword)

                # only chakk jehde running
                # if not Running then
                # chakk jehde Active with Low Count and Low PK
                if row is not None:
                    BotPhone = str(row[1])
                    BotPassword = str(row[2])
                    BotId = str(row[0])
                    BotCredentials  = (BotPhone,BotPassword)
                    # fetching admin phone number
                    adminNoStr = "select * from public.wbot_admin where id in( select admin_id_id from public.wbot_adminbot where bot_id_id = \'%s\' )"
                    cur.execute(adminNoStr %(BotId))
                    adminDetailsRow= cur.fetchone()
                    adminPhoneNumber= adminDetailsRow[1]
                    # got admin phone number
                    print (row)
                    try:
                        set_working_sql = "UPDATE  public.wbot_bot SET bot_state = 2 WHERE id = \'"+BotId+"\'"
                        cur.execute(set_working_sql)
                        conn.commit()
                        startBot(BotCredentials)
                    except AuthError:
                        # set bot number blocked
                        update_sql = " UPDATE  public.wbot_bot SET bot_state = 1  WHERE id = \'"+BotId+"\'"
                        cur.execute(update_sql,BotId)
                        conn.commit()
                        # send sms to  admin phone number
                        cur.close()
                        conn.close()
                        # Using Continue to restart
                        print('AuthError')
                        # time.sleep(2)
                        continue
                    except BotLimitReached:
                        cur.execute('update public.wbot_bot set bot_state = \'0\' where id = \'%s\''%(str(BotId)))
                        DB_CONNECTION.commit()
                        cur.execute('Select id,bot_phone,bot_pwd from public.wbot_bot where  bot_state = 0 order by  message_count asc')
                        row = cur.fetchone()
                        print(row)
                        BotPhone=str(row[1])
                        BotPassword = str(row[2])
                        BotId=str(row[0])
                        cur.execute('update public.wbot_bot set bot_state = \'2\' where id = \'%s\''%(str(BotId)))
                        conn.commit()
                        BotCredentials  = (BotPhone,BotPassword)
                        startBot(BotCredentials)







                else:
                    print('No bot available')
                    if conn is not None:
                        conn.close()
                    # no bot available
                    # call main() again or goto start
                    continue
            else:
                print('Database not Connected')
                if conn is not None:
                    conn.close()

                # Using Continue to restart
                continue
        except KeyboardInterrupt:
            print('Exited')
            if conn is not None:
                conn.close()
            break

        # except :
        #     print('An Unknown Exception has been Encountered . Sending Sms To Developers')
        #     if conn is not None:
        #         conn.close()
        # #    continue
        #     break
            # send SMS to developers
            # continue
            # Continue the execution





if __name__=="__main__":
    main()
