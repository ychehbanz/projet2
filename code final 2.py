import board
import displayio
import terminalio
import busio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from analogio import AnalogIn
import pwmio
import time


cp_in=AnalogIn(board.A0)
cp_out=pwmio.PWMOut(pin=board.GP0,frequency = 1000 , duty_cycle=0)
cp_out.duty_cycle=int(20/100*65535)


displayio.release_displays()
spi = busio.SPI(clock=board.GP18,MOSI=board.GP19,MISO=board.GP16)
oled_reset = board.GP20
oled_cs = board.GP17

oled_dc = board.GP21
display_bus = displayio.FourWire(spi, command=oled_dc, chip_select=oled_cs,
reset=oled_reset, baudrate=1000000)

WIDTH = 128
HEIGHT = 64 # Change to 64 if needed
BORDER = 5
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
splash = displayio.Group()
display.show(splash)

text= "borne de recharge\nVehicule debranche\nVeuillez Branchee "
ecran1 = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=10, y=20 // 2 - 1)





def lecture_etat_cp(tension):
    if tension>2.50:
        etat= "A"
    elif tension<2.50 and tension>2.15:
        etat= "B"
    elif tension<2.2 and tension > 1.80:
        etat= "C"
    return (etat)


splash.append(ecran1)
Etat_actif ="VE debrancher"

while True:

    print(cp_in.value)
    tension=(3.3*cp_in.value)/65535

    print(tension)
    print(lecture_etat_cp(tension))
    print (Etat_actif)


    time.sleep(1)
    etat_cp = lecture_etat_cp(tension)

    if Etat_actif== "VE debrancher" and etat_cp== "B" :
        Etat_actif= "VE_branché_déconnecté"


    if (Etat_actif== "VE_branché_déconnecté" or Etat_actif=="Erreur") and etat_cp== "C":
        Etat_actif= "VE_connecté"


    if (Etat_actif== "VE_connecté" or Etat_actif=="Erreur") and etat_cp== "A" :
        Etat_actif= "VE debrancher"

    if Etat_actif== "VE_connecté" and etat_cp== "B" :
         Etat_actif= "Erreur"


    #Action
    if Etat_actif == "VE_branché_déconnecté":
        ecran1.text ="borne de  recharge \n Vehicule branche \n attente de connexion"

    if Etat_actif== "VE debrancher":
        ecran1.text="borne de  recharge \n Vehicule debranche \n Veuillez Branchee "

    if Etat_actif== "VE_connecté":
        ecran1.text="borne de  recharge \n Vehicule connecté \n en charge"

    if Etat_actif== "Erreur":
        ecran1.text="borne de  recharge \n Vehicule connecté \n Charge arretée par VE"
