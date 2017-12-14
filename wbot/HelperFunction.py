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

        if len(datasplit) > 1:
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





def registercode(phone,cc,code):
    process=subprocess.Popen(["yowsup-cli","registration","-R",code,"-p",phone,"-C",cc],stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)
    output=output.decode('ASCII')
    output=output[output.find('\n\n\n'):]
    output=output[3:-1]
    output=output.split('\n')
    dictionary_ = {}
    print(output,error)
    for data in output:
        datasplit=data.split(':')
        print(datasplit)
        if len(datasplit) > 1:
            dictionary_[datasplit[0]]=str(datasplit[1])[datasplit[1].find('\''):]

    print(dictionary_)
    return dictionary_
    # print(dictionary_)
    # try:
    #     if dictionary_['status']=="'ok'":
    #         try:
    #             password=dictionary_['pw']
    #             print("password = "+password)
    #         except KeyError:
    #             print('Number REgistration Failure')
    #     elif dictionary_['status']=="'fail'":
    #         print("Wrong Code Enter Correct one")
    # except KeyError:
    #     print('Server Error')
