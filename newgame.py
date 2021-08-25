import random, time




spelldic1 = {
    "Fireball": list(range(5, 10)),
    "Lightning Bolt": list(range(4, 9))
}
weapondic = {
    "axe": list(range(5, 7)),
    "bow": list(range(3, 9))
}



def weaponchoice():
    x = input("Please Enter the weapon you want to be informed of: [axe, bow]       | Enter 'Exit' to cancel.")
    if x == "bow":
        print("The Damage of the Bow is " + str(weapondic.get("bow")))
        time.sleep(2.0)
        x = input("Do you want to choose this weapon? Yes or No")
        if x == "Yes":
            x = weapondic("bow")
            chosenbow = x
            spellchoice()
        elif x == "No":
            weaponchoice()
        else:
            print("Try again")
        
    elif x == "axe":
        print("The Damage of the Axe is " + str(weapondic.get("axe")))
        time.sleep(2.0)
        x = input("Do you want to choose this weapon? Yes or No")
        if x == "Yes":
            x = weapondic("axe")
            chosenaxe = x
            spellchoice()
        elif x == "No":
            weaponchoice()
    elif x == "Exit":
        print("Closing...")
        time.sleep(3.0)
    else:
        print("Try entering a weapon")
        weaponchoice()

weaponchoice()

def spellchoice

#print(random.choice(x))
#print("Your Damage is " + str(weapondic["axe"]))