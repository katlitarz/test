from flask import Flask, request, jsonify
import json, http.client, requests

def get_token():    #Get Access Token (Authorization Token)
    token_url = "https://cpgroup-h1.ekoapp.com/oauth/token"

    #client (application) credentials on apim.byu.edu
    client_id = "88711374-30f9-432e-8d64-4ca0c390e958" #mr.infra
    client_secret = "d0e178a2420b3f943f151dceb6a134f4e28caf64"

    #step A, B - single call with client credentials as the basic auth header - will return access_token
    data = {'grant_type': 'client_credentials','scope':'bot'}


    access_token_response = requests.post(token_url, data=data,verify=False, allow_redirects=False, auth=(client_id, client_secret))

    tokens = json.loads(access_token_response.text)
    
    return(tokens['access_token'])



def chat(replyToken,msg):
    conn = http.client.HTTPSConnection("cpgroup-h1.ekoapp.com")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append('--' + boundary)
    dataList.append('Content-Disposition: form-data; name=message;')

    dataList.append('Content-Type: {}'.format('multipart/form-data'))
    dataList.append('')

    dataList.append(msg)
    dataList.append('--' + boundary)
    dataList.append('Content-Disposition: form-data; name=replyToken;')

    dataList.append('Content-Type: {}'.format('multipart/form-data'))
    dataList.append('')

    dataList.append(replyToken)
    dataList.append('--'+boundary+'--')
    dataList.append('')
    body = '\r\n'.join(dataList)
    payload = body
    bearer = get_token()
    headers = {
    'Authorization': 'Bearer '+ bearer ,
    #  'Content-Type': 'multipart/form-data',
    'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/bot/v1/message/text", payload.encode("utf-8"), headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

    return() 



app = Flask(__name__)

@app.route('/bot/', methods=['POST'])
def get_evnt():
    targetIP =""
    subnet = ""
    count = 0
    match_subnet = 0
    match_hostname = 0
    match_input_hostname = 0
    sending_msg = ""
    hostname = ""
    output_hostname = ""
    siteTel = ""
    cText1 = ""
    cText2 = ""
    numip = ""
    split_numip = ""
    output_owner = ""
    output_OS_Version = ""
    output_Location = ""
    count_location = 0
    match_location = 0
    match_count = 0
    match_tel = 0
    
    req_data = request.get_json()
    events = req_data['events'][0]
    print(events)
    typ = events['type']
    replyToken = events['replyToken']
    print(replyToken)
    if (typ == "join"):         #กดJoin
        chat(replyToken,"Hello!!")
    elif (typ == "message"):    #พิมข้อความ
        message = events['message']['text']
        
        # เปิดถาม ด้วย : 
        if message[0] == ":" :
            message = message[1:]
            # *************Condition 1 => Count ****************
            if (message == "count" or message == "Count" ) :
                sending_msg = "Please Input Number "+ "\n" +":1. Thailand-On Premise"+ "\n" + ":2. On Cloud" +"\n" + ":3. Vietnam-On Premise" + "\n" + ":4. Turkey-On Premise"
                match_count = 1
            #message = input("input :")
            #1. Thailand-On Premise
            elif(message == "1" or message == "1." ):
                message = "Thailand - On Premise"
                match_location = 1
                hostfile = open("hostname.txt",'r',encoding='utf8')
                for line2 in hostfile:
                    hlist = []
                    for item2 in line2.split(','):
                        hlist.append(item2.strip())
                    if(message == hlist[11]):
                        count_location += 1
                        #print(count_location)
                        sending_msg = count_location,". ",hlist[1]
                        if(match_location == 1):
                            chat(replyToken,sending_msg)
                        else:
                            chat(replyToken,"No match record")
                        
                hostfile.close()
                
                sending_msg = "Thailand -On Premise " +"\n"
                sending_msg = sending_msg + "Count : %d Servers" %count_location
                match_location = 1

                

            #2. On Cloud
            elif(message == "2" or message == "2." ):
                message = "On Cloud"
                hostfile = open("hostname.txt",'r',encoding='utf8')
                for line2 in hostfile:
                    hlist = []
                    for item2 in line2.split(','):
                        hlist.append(item2.strip())
                    if(message == hlist[11]):
                        count_location += 1
                        #print(count_location)
                hostfile.close()
                sending_msg = "On Cloud " +"\n"
                sending_msg = sending_msg + "Count : %d Servers" %count_location
                match_location = 1
                print(sending_msg)

            # 3. Vietnam-On Premise
            elif(message == "3" or message == "3." ):
                message = "Vietnam - On Premise"
                hostfile = open("hostname.txt",'r',encoding='utf8')
                for line2 in hostfile:
                    hlist = []
                    for item2 in line2.split(','):
                        hlist.append(item2.strip())
                    if(message == hlist[11]):
                        count_location += 1
                        #print(count_location)
                hostfile.close()
                sending_msg = "Vietnam -On Premise " +"\n"
                sending_msg = sending_msg + "Count : %d Servers" %count_location
                match_location = 1
                print(sending_msg)

            #4. Turkey-On Premise
            elif(message == "4" or message == "4." ):
                message = "Turkey - On Premise"
                hostfile = open("hostname.txt",'r',encoding='utf8')
                for line2 in hostfile:
                    hlist = []
                    for item2 in line2.split(','):
                        hlist.append(item2.strip())
                    if(message == hlist[11]):
                        count_location += 1
                        #print(count_location)
                hostfile.close()
                sending_msg = "Turkey -On Premise " +"\n"
                sending_msg = sending_msg + "Count : %d Servers" %count_location
                match_location = 1
                print(sending_msg)        
        
                   
            #****************Condition 2 ถาม IP บอก Detail ถ้า IP ตรงจะบอก Hostnameด้วย****************
            #Condition 2.1 : Input => :IP:10.1.117.250       
            
            ifIP = message.split(':')
            if(ifIP[0]=="ip" or ifIP[0]=="IP" or ifIP[0]=="Ip" or ifIP[0]=="iP"):   #เงื่อนไข1 พิมIP ,ifIP[0] = IP
                targetIP = ifIP[1]  #เลขIP
                subN = ifIP[1].split('.') #subN เลขIP split ด้วย '.'  192  168  70  71
                subnet = subN[0]+'.'+subN[1]+'.'+subN[2]+".0"   # subnet = เลขIPลงท้ายด้วย0
                
            #**************** Condition 2.2 : input => 10.1.117.250 (ไม่ต้องใส่ IP:)    ****************
            for i in range(len(message)):
                c = message[i]
                if c == "." :
                    count += 1
            ifIP = message.split(':')
            if (count ==3 and ifIP[0]!="ip" and ifIP[0]!="IP" and ifIP[0]!="Ip" and ifIP[0]!="iP" ):
                numip = message.split('.')
                split_numip = numip[0]+'.'+numip[1]+'.'+numip[2]+'.'+numip[3]
                targetIP = split_numip    #เลขIP
                subnet = numip[0]+'.'+numip[1]+'.'+numip[2]+'.0'    # subnet = เลขIPลงท้ายด้วย0
            
            #wanLink ข้อมูล subnet = เลขIPลงท้ายด้วย0
            #ใช้ wanLink ต่อเมื่อ input IP มา
            if subnet != "" :
                wanLink = open("Wanlink.txt",'r',encoding='utf8')
                for line in wanLink:        #line = วนแต่ละแถวของไฟล์ wanLink
                    flist = []              #ตัวแปร list
                    for item in line.split(','):    #item แต่ละ คือ Subnet_IP,Location,Office Phone,Contact1,Mobile,Contact2,Mobile (split(','))
                        flist.append(item.strip())  #แต่ละitem ไปเก็บไว้ในlist ตัวแปร flist
                    if(subnet == flist[0]):         # subnet = เลขIPลงท้ายด้วย0   (จากinput)  ,  flist[0] = เลขIPลงท้ายด้วย0 (จากในไฟล์)
                        match_subnet = 1            # ********* subnet(input) = subnet(File) *********
                        location = flist[1]         #ข้อมูลlocation ในไฟล์
                        if(flist[2]!=""):           #flist[2] = Office Phone
                            siteTel = flist[2]      #Office Phone
                        if(flist[3]!=""):           #flist[3] = Contact1, flist[4] = Mobile
                            cText1 = flist[3]+"\nTel: "+ flist[4]   # cText1 =  Contact1 + Tel: Mobile
                        if(flist[5]!=""):                           #flist[5] = Contact2 #flist[6] = Mobile
                            cText2 = flist[5]+"\nTel: "+ flist[6]   # cText2 =  Contact2 + Tel: Mobile
                        break
                wanLink.close()
            
            #ข้อมูล hostfile => targetIP
            hostfile = open("hostname.txt",'r',encoding='utf8')
            for line2 in hostfile:                  #คือ 10.1.208.44,dbora-bnu01 ของ hostfile (วนแต่ละแถวของไฟล์)
                hlist = []                          #Type list
                for item2 in line2.split(','):      #คือ 10.1.208.44  กับ dbora-bnu01 ของ 10.1.208.44,dbora-bnu01 (วน 2 ครั้ง)
                    hlist.append(item2.strip())     #คือ hlist ที่เป็น List [10.1.208.44,dbora-bnu01] (ไม่มี , แล้ว,)
                if(targetIP == hlist[0]):           # hlist[0] = เลขIP
                    match_hostname = 1              # ********* เลขIP(input) = เลขIP(File) *********
                    hostname = hlist[1]             #hlist[1] คือ hostname
                    output_owner = hlist[9]
                    output_OS_Version = hlist[10]
                    output_Location = hlist[11]
                    break
            hostfile.close()
            
            #**************** Condition 3 ถาม hostname บอก IP ****************
            hostfile = open("hostname.txt",'r',encoding='utf8')
            for line2 in hostfile:
                hlist = []
                for item2 in line2.split(','):
                    hlist.append(item2.strip())
                if(message == hlist[1] or message == hlist[2] or message ==  hlist[3] or message ==  hlist[4] or message ==  hlist[5] or message ==  hlist[6] or message ==  hlist[7] or message ==  hlist[8]):
                #if(message == hlist[1] or hlist[2] or hlist[3] or hlist[4] or hlist[5] or hlist[6]):		# hlist[0] คือ IP, hlist[1-8] คือ hostname
                    output_hostname = hlist[0]
                    output_owner = hlist[9]
                    output_OS_Version = hlist[10]
                    output_Location = hlist[11]
                    match_input_hostname = 1            # *********hostname = hostname(File)*********
                    break
            hostfile.close()
            
            # *************** condition 4 Tel ***************
            #input
            #1. name [1]
            #2. nickname [3]

            #message = input("input :")
                          
            Tel_Infra_file = open("Tel_Infra.txt",'r',encoding='utf8')
            for line in Tel_Infra_file:     #line คือ ทั้งแถว (1 loop ต่อ 1 แถว)
                list_tel = []
                for item in line.split(','):   #item คือ แต่ละ column ของ1แถว
                    list_tel.append(item.strip()) #แต่ละ item เก็บใน list_tel  ของ1แถว  :Array [0-7]
                    
                #1. name [1]
                if message == list_tel[1] :     #name [1]
                    match_tel = 1
                    sending_msg = "Full Name : " + list_tel[0] + "\n"           #full_name[0]
                    sending_msg = sending_msg + "Nickname : " + list_tel[3] + "\n"            #nickname [3]
                    sending_msg = sending_msg + "Office Tel : " + list_tel[4] + "\n"          #office[4]
                    sending_msg = sending_msg + "Tel : " + list_tel[5] + "\n"                 #number[5]
                    sending_msg = sending_msg + "Tel Home : " + list_tel[6] + "\n"            #tel_home[6]
                    sending_msg = sending_msg + "Other Tel : " + list_tel[7] + "\n"           #other_tel[7]
                    if(match_tel == 1):
                        chat(replyToken,sending_msg)
                    else:
                        chat(replyToken,"No match record")
                                          
                #2. nickname [3]
                if message == list_tel[3] :     #nickname [3]
                    match_tel = 1
                    sending_msg = "Full Name : " + list_tel[0] + "\n"           #full_name[0]
                    sending_msg = sending_msg + "Nickname : " + list_tel[3] + "\n"            #nickname [3]
                    sending_msg = sending_msg + "Office Tel : " + list_tel[4] + "\n"          #office[4]
                    sending_msg = sending_msg + "Tel : " + list_tel[5] + "\n"                 #number[5]
                    sending_msg = sending_msg + "Tel Home : " + list_tel[6] + "\n"            #tel_home[6]
                    sending_msg = sending_msg + "Other Tel : " + list_tel[7] + "\n"           #other_tel[7]
                    if(match_tel == 1):
                        chat(replyToken,sending_msg)
                    else:
                        chat(replyToken,"No match record")
                    
            Tel_Infra_file.close()

            
            #*************************Result*************************
            # Condition 2 ถาม IP บอก Detail ถ้า IP ตรงจะบอก Hostnameด้วย
            #(Input IP)     
            if(match_hostname == 1):               # *** เลขIP(input) = เลขIP(File) ***
                sending_msg = "IP: "+targetIP+"\n"
                sending_msg = sending_msg+"Hostname: "+hostname+"\n"
                sending_msg = sending_msg+"Owner: "+output_owner+"\n"
                sending_msg = sending_msg+"OS Version: "+output_OS_Version+"\n"
                sending_msg = sending_msg+"Location: "+output_Location+"\n"
                print(sending_msg)
            if(match_subnet==1):                    # *** subnet(input) = subnet(File) ***
                sending_msg = "IP: "+targetIP+"\n"
                sending_msg = sending_msg+"Hostname: "+hostname+"\n"
                sending_msg = sending_msg+"Location: "+location+"\n"
                if(siteTel!=""):
                    sending_msg = sending_msg + "Site Tel: " + siteTel+"\n"
                if(cText1!=""):
                    sending_msg = sending_msg + "Contect Person: " + cText1+"\n"
                if(cText2!=""):
                    sending_msg = sending_msg + "Contect Person2: " + cText2+"\n"
                print(sending_msg)
             
            #Condition 3 hostname บอก IP
            #(Input hostname)
            if(match_input_hostname == 1):      # *** hostname(input) = hostname(File) ***
                sending_msg = "Hostname: "+message+"\n"
                sending_msg = sending_msg +"IP : "+ output_hostname+"\n"
                sending_msg = sending_msg +"Owner : "+ output_owner+"\n"
                sending_msg = sending_msg+"OS Version: "+output_OS_Version+"\n"
                sending_msg = sending_msg+"Location: "+output_Location+"\n"
                print(sending_msg +"IP : "+ output_hostname)
                                     
             #=============================*********Reply*********  ======================================
            if(match_hostname == 1 or match_subnet == 1 or match_input_hostname == 1 or match_location == 1 or match_count == 1 ):
                chat(replyToken,sending_msg)
            elif (match_tel == 1):
                pass               
            else:
                chat(replyToken,"No match record")
         
        #-------------------------------------------------------------------------------------------------         
   
        
    response = {}

    return (response)




# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True, port=5000)
