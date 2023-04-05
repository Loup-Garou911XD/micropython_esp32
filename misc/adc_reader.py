from machine import Pin, ADC
from time import sleep_ms

pin_no = 34
piezo = ADC(Pin(pin_no))
piezo.atten(ADC.ATTN_2_5DB)


while True:
    piezo_value = piezo.read()
    print(piezo_value)
    sleep_ms(20)
