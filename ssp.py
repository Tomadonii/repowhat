import random, time

def ssp():
    x = ("schere", "stein", "papier")
    antwort = input("Möchtest du eine Runde SSP spielen? [yes | no] ")
    while antwort == "yes":
        waffen = input("Treffe bitte deine Wahl zwischen schere, stein und papier!: ")
        if waffen == "stein":
            
            time.sleep(0.2)
            arten = random.choice(x)
            
            if arten == "schere":
                antwort = input("Du hast gewonnen. Willst du nocheinmal spielen? [yes | no] ")
                if antwort == "yes":
                    print("Dann weiter")
                elif antwort == "no":
                    break
            
            if arten == "stein":
                antwort = input("Unentschieden. Willst du nochmal spielen? [yes | no] ")
                if antwort == "yes":
                    print("Dann weiter")
                elif antwort == "no":
                    break
            
            if arten == "papier":
                antwort = input("Du hast verloren. Willst du nochmal spielen? [yes | no] ")
                if antwort == "yes":
                    print("Dann weiter")
                elif antwort == "no":
                    break

        if waffen == "schere":
            
            time.sleep(0.2)
            arten = random.choice(x)
            
            if arten == "schere":
                antwort = input("Unentschieden. Nochmal? [yes | no]") 
                if antwort == "yes":
                    print("Dann weiter")
                elif antwort == "no":
                    print("Was zitterst denn so?")
                    break

            if arten == "papier":
                antwort = input("You won... but at what cost? Willst du nochmal spielen? [yes | no]")
                if antwort == "yes":
                    print("Dann weiter")
                elif antwort == "no":
                    print("Pathetic.")
                    break
            
            elif arten == "stein":
                antwort = input("Bist'n Loser kriegst nie n Preis. Nochma? [yes | no]")
                if antwort == "yes":
                    print("Dann weiter")
                elif antwort == "no":
                    print("Dann net")
                    break
        
        elif waffen == "papier":
            
            time.sleep(0.2)
            arten = random.choice(x)
            
            if arten == "schere":
                antwort = input("Idiot! [yes | no] ")
                if antwort == "yes":
                    print("Dann weiter")
                elif antwort == "no":
                    print("Thats what i thought.")
                    break
            
            if arten == "stein":
                antwort = input("Das war nicht fair! Nochmal! [yes| no] ")
                if antwort == "yes":
                    print("Dann weiter")
                elif antwort == "no":
                    print("Coward.")
                    antwort = input("Komm schon eine Runde noch! [yes | no] ")
                    if antwort == "yes":
                        print("Dann weiter")
                    elif antwort == "no":
                        print("Hast wohl Angst zu verlieren.")
                        break

            if arten == "papier":
                antwort = input("Joa ne, eigenlich müssen wir nochmal spielen, oder? [yes | no] ")
                if antwort == "yes":
                    print("Dann weiter")
                elif antwort == "no":
                    print("Jetzt gibts halt keinen Gewinner, aber okay.")
                    break
ssp()
             

