import machine, utime, json
from phew import server, connect_to_wifi
from picozero import pico_led

NETWORK = ("VM3222401", "hn7HrhvvMyvb")

ip = connect_to_wifi(NETWORK[0], NETWORK[1])
print(ip)

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
                
server.run()