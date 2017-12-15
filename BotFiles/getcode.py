import subprocess
 
    
    
def registercode(phone,cc,code):
    process=subprocess.Popen(["yowsup-cli","registration","-R",code,"-p",phone,"-C",cc],stdout=subprocess.PIPE)
    output, error = process.communicate()
    output=output.decode('ASCII')
    output=output[output.find('\n\n\n'):]
    output=output[3:-1]
    output=output.split('\n')
    print('OUTPUT:')
    dictionary_ = {}
    for data in output:
        datasplit=data.split(':')
        dictionary_[datasplit[0]]=str(datasplit[1])[datasplit[1].find('\''):]
    print(dictionary_)
    try:
        if dictionary_['status']=="'ok'":
            try:
                password=dictionary_['pw']
                print("password = "+password)
            except KeyError:
                print('Number REgistration Failure')
        elif dictionary_['status']=="'fail'":
            print("Wrong Code Enter Correct one")
    except KeyError:
        print('Server Error')
        
    
    #{'status': "'ok'", 'login': "'917888993850'", 'pw': "'pzj/o4js8oIujEQxuHhs+N/TjS4='", 'cost': "'0.99'", 'expiration': '0', 'currency': "'USD'", 'type': "'existing'", 'kind': "'free'", 'price': "'$0.99'", 'price_expiration': '1'}

    


def getcode(phone,cc,mode="sms"):
    process = subprocess.Popen(["yowsup-cli","registration","-p",phone,"-C",cc,"-r",mode,"-E","android"], stdout=subprocess.PIPE)
    output , err = process.communicate()
    output=output.decode('ASCII')
    output=output[output.find('\n\n\n'):]
    output=output[3:-1]
    output=output.split('\n')
    print('OUTPUT:')
    dictionary_ = {}
    for data in output:
        datasplit=data.split(':')
        dictionary_[datasplit[0]]=str(datasplit[1])[datasplit[1].find('\''):]
    #output=output[output.find('status'):]
    #output=output[output.find('b\''):]
    try:
        if dictionary_['status']=="'sent'":
            print("Send Success")
    
        if dictionary_['status']=="'fail'":
            print("Send failure")
            try:
                if dictionary_['reason']=="'too_recent'":
                    print("Hold on an hour")
                if dictionary_['reason']=="'blocked'":
                    print('Number has been blocked')
                elif dictionary_['reason']=="'bad_param'":
                    print('PhoneNumber not valid')
            except KeyError:
                print ("Unknown Error Occured")
                
        
        
    except KeyError:
        print('WhatsApp Servers Are Busy')
    
    
   

def main():
    phone = input()
    cc= '91'
    mode = 'sms'
    getcode(phone,cc,mode)
    
    
if __name__=='__main__':
    main()
