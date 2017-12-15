__author__ = 'charanjit'

from yowsup.stacks import  YowStackBuilder
from testlayer import Whatsbot
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env import YowsupEnv
from config import Config
import psycopg2
import subprocess
def startBot(credentials):
    print (credentials)
    stackBuilder = YowStackBuilder()
    stack = stackBuilder \
        .pushDefaultLayers(True) \
        .push(Whatsbot) \
        .build()
    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal
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
                cur.execute('Select id,bot_phone,bot_pwd from public.wbot_bot where bot_state = 0 order by  id asc')
                row = cur.fetchone()
                if row is not None:
                    BotPhone = str(row[1])
                    BotPassword = str(row[2])
                    BotId = str(row[0])
                    BotCredentials  = (BotPhone,BotPassword)
                    # fetching admin phone number
                    adminNoStr = "select * from public.wbot_admin where id in( select admin_id_id from public.wbot_adminbot where bot_id_id = " +BotId +")"
                    cur.execute(adminNoStr)
                    adminDetailsRow= cur.fetchone()
                    adminPhoneNumber= adminDetailsRow[1]
                    # got admin phone number
                    print (row)
                    try:
                        startBot(BotCredentials)
                    except AuthError:
                        # set bot number blocked
                        update_sql = """
                        UPDATE  public.wbot_bot
                        SET bot_state = 1
                        WHERE id = %s
                        """
                        cur.execute(update_sql,BotId)
                        conn.commit()
                        # send sms to  admin phone number
                        cur.close()
                        conn.close()
                        # Using Contninue to restart
                        continue
                        print('AuthError')
                else:
                    print('No bot available')
                    # no bot available
                    # call main() again or goto start
                    continue
            else:
                print('Database not Connected')

                # Using Contninue to restart
                continue
        except KeyboardInterrupt:
            print('Exited')
            break
        except:
            print('An Unknown Exception has been Encountered . Sending Sms To Developers')
            # send SMS to developers
            continue
            # Continue the execution





if __name__=="__main__":
    main()
