#DSMR P1 uitlezen
#Landis+Gyr E350 (DSMR 4.0)
#(c) E.C. Boeracker mrt 2017
versie = "0.9"
import sys
import serial

###
#error display
###
def show_error():
	ft = sys.exc_info()[0]
	fv = sys.exc_info()[1]
	print("Fout type: %s"%ft)
	print("Fout waarde: %s"% fv)
	return

###
#main program
###
print ("DSMR P1 uitlezen", versie)
print ("energie verbruik in kWh en gas in m3")
print ("Control-C om te stoppen")

#Configuratie seriele poort
ser = serial.Serial()
ser.baudrate = 115200
ser.parity=serial.PARITY_NONE
#ser.stopbits = serial.STOPBITS_one
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyAMA0"

#open com port
try:
	ser.open()
except:
	sys.exit ("Fout bij openen seriele poort %s." % ser.name)

#Initialize 
# Een data telegram telt 27 regels p1_teller 0 - 26
p1_teller=0
telegram=[]

while p1_teller < 26:
	p1_line=''
#Read first line
	try:
		p1_raw = ser.readline()
	except:
		sys.exit ("Seriele poort %s kan niet worden gelezen." % ser.name)
	p1_str=str(p1_raw)
#	p1_str=str(p1_raw,"utf-8")
	p1_line=p1_str.strip()
	telegram.append(p1_line)
#show all output from P1, make comment if not
	print (p1_line)
	p1_teller = p1_teller + 1
#betekenis telegram
#let op voor stroom geruik je posities 0-9
#voor gas 0-10
# eigenlijk logisch... je controlleert op meer
#0-0:1.0.0	datumtijd + zomer(S)/wintertijd(W) YYMMDDhhmmssX
#1-0:1.8.1	totaleverbruik tarief 1 kWh (hoog) YYYYYY.YYY
#1-0:1.8.2	totaleverbruik tarief 2 kWh (laag) YYYYYY.YYY
#1-0:2.8.1	totale teruglevering tarief 1 kWh (hoog) YYYYYY.YYY
#1-0:2.8.2	totale teruglevering tarief 2 kWh (laag) YYYYYY.YYY
#0:96.14.0	actueel tarief: 1 = tarief 1, 2 = tarief 2
#1-0:1.7.0	actueel verbruik (+P) (kW), YY.YYY
#1-0:2.7.0	actuele teruglevering (-P) (kW), YY.YYY
#0-1:24.2.1	datumtijd+zomer(S)/wintertijd(W)+gasverbruik (m3) YYMMDDhhmmssX + YYYYY.YYY
#0-1:24.3.0	gasverbruik

#juiste regels ophalen
telegram_teller=0
while telegram_teller < 26:
#	print "telegram regel",telegram[telegram_teller][0:10]
#laag verbruik
	if telegram[telegram_teller][0:9] == "1-0:1.8.1":
		print "totaal verbruik dal		",telegram[telegram_teller][10:20]," kWh"
#hoog verbruik
	elif telegram[telegram_teller][0:9] == "1-0:1.8.2":
		print "totaal verbruik hoog		",telegram[telegram_teller][10:20], " kWh"
#hoog teruglevering
	elif telegram[telegram_teller][0:9] == "1-0:2.8.1":
		print "Totaal teruglevering dal	",telegram[telegram_teller][10:20]," kWh"
#hoog tarief teruglevering
	elif telegram[telegram_teller][0:9] == "1-0:2.8.2":
		print "Totaal teruglevering hoog	",telegram[telegram_teller][10:20]," kWh"
#actueel stroomverbruik
	elif telegram[telegram_teller][0:9] == "1-0:1.7.0":
		print "actueel stroomverbruik +P	",telegram[telegram_teller][10:16]," kW"
#actueel teruggeleverd vermogen (-P)
	elif telegram[telegram_teller][0:9] == "1-0:2.7.0":
		print "actueel teruglevering -P	",telegram[telegram_teller][10:16]," kW"
#Gasmeter
	elif telegram[telegram_teller][0:10] == "0-1:24.2.1":
		print "gasverbruik		 	",telegram[telegram_teller][26:35]," m3"
	else:
		pass
	telegram_teller = telegram_teller + 1
#print (stack, "\n")

#Close serial port and show status
try:
	ser.close()
except:
	sys.exit ("Foutje %s. Programma afgebroken. Seriele poort kon niet gesloten worden." % ser.name)

