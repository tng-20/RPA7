import machine, utime, json
import network
from phew import server, connect_to_wifi, get_ip_address
from picozero import pico_led

SSID = "terence"
PASS = "1616hh^**^"

connect_to_wifi(SSID, PASS)
wlan = network.WLAN(network.STA_IF)
print("connected:", wlan.isconnected())
print("config:", wlan.ifconfig())
print(get_ip_address())

def digital(data: ADC):
    return True if data.read_u16() > 5000 else False

@server.route("/api/data", methods=["GET"])
def getData(request):
    pico_led.on()
    count = 0
    first = 0
    last = 0
    data = machine.ADC(26)
    old = digital(data)
    while count < 3:
        if old != digital(data):
            old = not old
            if old:
                count += 1
            if count == 1:
                first = utime.time_ns()
            if count == 3:
                last = utime.time_ns()
        utime.sleep_us(5)
    period = (last - first)/1000000000
    pico_led.off()
    return json.dumps({"period": period}), 200, {"Content-Type": "application/json"}

@server.route("/api/ping", methods=["GET"])
def ping(request):
    return "okay"
                
server.run()