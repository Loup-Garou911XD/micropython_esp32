import network
import time
import _thread
from misc import led
from misc import saved_networks

print("	[32m[bootstrap.sta_if][0m")

silent = False  # no output if True
ssids = {}
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
saved_networks = saved_networks.saved_networks


def do_connect(iface, ssid, key,silent=False):
    if not iface.isconnected():
        if not silent:
            print("\n", f"connecting to {ssid}...")
        iface.connect(ssid, key)
        # while not wlan.isconnected():
        #   pass


def do_scan():
    global ssids
    scan_result = wlan.scan()
    for i in ssids.keys():
        ssids[i] = False

    for j in scan_result:
        ssids[str(j[0], "UTF-8")] = True


def main(silent=False):
    with led.BlinkLed():
        try:
            while not wlan.isconnected():
                if wlan.status() == 1001:
                    time.sleep_ms(50)
                    continue

                do_scan()
                connectable = []

                for i in saved_networks.keys():
                    if i in ssids.keys():
                        connectable.append(i)
                if connectable:
                    
                    do_connect(wlan, 
                               connectable[-1],
                               saved_networks[connectable[-1]], # -1 for the 1st network in saved_network
                               silent)
                    
            if not silent:
                if_config = wlan.ifconfig()
                if_config = "\n\t\t".join(["", 
                                           "ip :"+"[44;1;97m"+if_config[0]+"[0m",
                                          "subnet_mask :"+if_config[1], 
                                          "gateway :"+if_config[2], 
                                          "dns :"+if_config[3] + "\n"
                                          ])

                print("\n\tnetwork config:", "[33m" +
                      wlan.config("essid")+"[0m", if_config)

        except KeyboardInterrupt:
            print("\033[91mConnecting in background\033[0m")
            if wlan.isconnected():
                wlan.disconnect() # resetting from previus unsuccessful connection
            _thread.start_new_thread(main, [True])


main()