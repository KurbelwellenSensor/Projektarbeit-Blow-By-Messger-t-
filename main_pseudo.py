#Einstellung
    #knopf 'an' pins benennen
    #knopf druck empfangen
    #system an

    #f0.1: OutputDisplay
        #pins vom Display benennen
        #print 'gerät an'  

    #f0.2: InputDruckunterschiedAnsaug
        #pins festlegen für sensor

    #f0.2: InputDruckunterschiedBlowby
        #pins festlegen für sensor

    #f0.3: InputTemperaturAnsaug
        #pins festlegen für sensor

    #f0.4: InputTemperaturHeizung 
        #pins festlegen für sensor
        #SollTemperatur festgelegt

    #f0.5: OutputHeizungRegler
        #pins festlegen für Outputsignal

    #f0.6: OutputEthernetBridge   
        #pins festlegen für Outputsignal

#MainLoop
        
    #f1: Signal emfangen

        #f1.1:  DruckunterschiedAnsaug
            #Digitales signal vom sensor bekommen
                #if signal == 0: print error2.1 'Drucksensorfehler'
            #Signal in Pascal umwandeln
            #wert speichern

        #f1.2:  DruckunterschiedBlowby
            #Digitales signal vom sensor bekommen
                #if signal == 0: print error2.1 'Drucksensorfehler'
            #Signal in Pascal umwandeln
            #wert speichern

        #f1.3:  Temperatur Ansaug
            #Digitales signal vom sensor bekommen
                #if signal == 0: print error2.2 'Temperatursensor1fehler'
            #Signal in Kelvin umwandeln
            #wert speichern

        #f1.4:  Temperatur Heizung 
            #Digitales signal vom sensor bekommen
                #if signal == 0: print error2.3 'Temperatursensor2fehler'
            #Signal in Kelvin umwandeln
            #wert speichern

        #f2: Heizung Regelung
            #if InputTemperaturHeizung >= SollTemperatur 
                #pinOutputHeizungRegler Signal 'Aus'
            #else
                #pinOutputHeizungRegler Signal 'An'

        #f3: Blow-by Wert berechnen
            #berechnungen aus MATLAB umschreiben
                #realistisches Wertbereich festlegen
                #if Blow-By ausser Wertbereich: print 'Volumentstrom unrealistisch'

            #f3.1 Fehler Berechnung
                #Fehlerverbreitung Berechnung
                    #if Fehler >= 0,1: print error3.1 'Fehler zu groß'

        #f4: Wert verpacken
            #Volumenstrom nehmen
            #in ethernet protokoll einbauen

        #f5: Wert abschicken
            #an den pins der Bridge signal schicken

        #print 'system läuft' for 1 second

        #if pin 'an' Knopf gedrückt
            #print 'system aus' for 2seconds
            #system aus
            
