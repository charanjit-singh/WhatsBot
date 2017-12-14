import subprocess



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
    return dictionary_
    #output=output[output.find('status'):]
    #output=output[output.find('b\''):]
    # try:
    #     if dictionary_['status']=="'sent'":
    #         print("Send Success")
    #
    #     if dictionary_['status']=="'fail'":
    #         print("Send failure")
    #         try:
    #             if dictionary_['reason']=="'too_recent'":
    #                 print("Hold on an hour")
    #             if dictionary_['reason']=="'blocked'":
    #                 print('Number has been blocked')
    #             elif dictionary_['reason']=="'bad_param'":
    #                 print('PhoneNumber not valid')
    #         except KeyError:
    #             print ("Unknown Error Occured")
    #
    #
    #
    # except KeyError:
    #     print('WhatsApp Servers Are Busy')
