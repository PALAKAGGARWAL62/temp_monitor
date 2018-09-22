import conf
from boltiot import Sms, Bolt, Email
import json, time
import tweepy

config = {
"consumer_key" : conf.consumer_key,
"consumer_secret" : conf.consumer_secret,
"access_token" : conf.access_token,
"access_token_secret" : conf.access_token_secret
    }

def get_api_object(cfg):
    auth =tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SSID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
mailer = Email(conf.MAILGUN_API_KEY, conf.SANDBOX_URL, conf.SENDER_EMAIL, conf.RECIPIENT_EMAIL)

response = mybolt.analogRead('A0') 
data = json.loads(response)
print ("Current Temperature is: %s" % data['value']) 
sensor_value = int(data['value']) 

minimum_limit = int(input("Enter minimun Threshold value for Temperature in Kelvin scale: "))
maximum_limit = int(input("Enter maximun Threshold value for Temperature in Kelvin scale: "))

if sensor_value > maximum_limit or sensor_value < minimum_limit:  
    api_object = get_api_object(config)
    tweet = "ALERT! The Current temperature sensor value is " +str(sensor_value)
    status = api_object.update_status(status=tweet)   

while True: 
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
    # print (data['value'])
    try: 
        sensor_value = int(data['value']) 
        print ("Current Temparature is: "+str(sensor_value))
        if sensor_value > maximum_limit or sensor_value < minimum_limit:
            response = sms.send_sms("The Current temperature sensor value is " +str(sensor_value)) 
            response = mailer.send_email("Alert", "The Current temperature sensor value is " +str(sensor_value))
            
    except Exception as e: 
        print ("Error",e)
    time.sleep(10)
