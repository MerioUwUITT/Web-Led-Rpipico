import netman
import secrets
import socket
from machine import Pin
from picozero impot RGBLED

led = Pin("LED",Pin.OUT)
rgb = RGBLED(red=0,green=1,blue=2)
country = "MX"
ssid = secrets.SSID
password = secrets.PASSWORD

wifi_connection = netman.connectWiFi(ssid,password,country)

html = """<!DOCTYPE html>
<html>
<head> <title>Pico W</title> </head>
<body> <h1>Pico W</h1>
<p>Current status: %s</p>
<p><a href="http://"""+wifi_connection[0]+"""/light/on">Turn ON</a></p>
<p><a href="http://"""+wifi_connection[0]+"""/light/off">Turn OFF</a></p>

</body>
</html>
"""
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

led.value(0)
stateis = "LED is OFF"

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)
    
        request = str(request)[0:50] # The [0:50] avoids getting the url directory from referer 
        led_status = request.find('GET / HTTP')
        led_on = request.find('/light/on')
        led_off = request.find('/light/off')
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))
    
        if led_status >0:
              print("LED status request") # No LED action

        if led_on >0:
              print("led on")
              led.value(1)
              stateis = "LED is ON"

        if led_off >0:
              print("led off")
              led.value(0)
              stateis = "LED is OFF"
      
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
    
    except OSError as e:
        cl.close()
        print('connection closed')    