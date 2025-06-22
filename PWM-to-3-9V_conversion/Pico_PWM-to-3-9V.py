from machine import Pin, PWM, time_pulse_us
import utime

# Määritellään mittauspinni (PWM-signaalin lukemiseen)
#----Pinni 15 on Picon vasemman alalaidan pinni
pwm_in = Pin(15, Pin.IN) 

# Määritellään ulostulopinni, jolla generoidaan "analoginen" jännite PWM:n avulla
#----Pinni 16 on Picon oikean alalaidan pinni
pwm_out_pin = Pin(16)
pwm_out = PWM(pwm_out_pin)
pwm_out.freq(1000)  # PWM-ulostulon taajuus (voit säätää tarpeen mukaan)

# 50 Hz:n jakson pituus mikrosekunteina
PERIOD_US = 20000

def read_pwm_pulse():
    """
    Mittaa PWM-signaalin HIGH-pulssin keston mikrosekunteina.
    Odotamme ensin, että signaali menee LOW-tasoon ennen mittauksen aloittamista.
    """
    # Looppi odottoo, että pwm_in on HIGH tilassa
    while pwm_in.value() == 1:
        pass
    # Mitataan HIGH-tason kesto.
    pulse_us = time_pulse_us(pwm_in, 1, PERIOD_US*1.5) # Argumentit: Mitataan HIGH pulssia, Odotetaan enintään 1.5 jaksoa
    return pulse_us

while True:
    pulse_width = read_pwm_pulse()  # Pulssin pituus mikrosekunteina
   
   
    # Rajataan mahdolliset poikkeavat arvot välille 1000-2000 µs
    if pulse_width < 1000:
        pulse_width = 1000
    elif pulse_width > 2000:
        pulse_width = 2000
    
    # Määritellään lineaarinen muunnos:
    # Kun pulse_width on 1000 µs, ulostulon duty on 0.25 (25%)
    # Kun pulse_width on 2000 µs, ulostulon duty on 0.75 (75%)
    duty_out = 0.25 + ((pulse_width - 1000) / 1000) * 0.5

    # Muutetaan 0.0-1.0 duty-arvo 16-bittiseksi PWM-arvoksi (0–65535)
    duty_out_u16 = int(duty_out * 65535)
    pwm_out.duty_u16(duty_out_u16)
    
    print("Pulssin pituus: {} µs, ulostulo: {:.1f}% maksimijännitteestä".format(pulse_width, duty_out * 100))
    utime.sleep(0.5)
