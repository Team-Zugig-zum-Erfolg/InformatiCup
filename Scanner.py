Tstring = '# Strecken: str(ID) str(Anfang) str(Ende) dec(LÃ¤nge) int(KapazitÃ¤t)'
Trainstring = '# ZÃ¼ge: str(ID) str(Startbahnhof)/* dec(Geschwindigkeit) int(KapazitÃ¤t)'
Passengersstring = '# Passagiere: str(ID) str(Startbahnhof) str(Zielbahnhof) int(GruppengrÃ¶ÃŸe) int(Ankunftszeit)'



Trainstations = []  
Trains = []
Passengers = []


mylines = []                                # Declare an empty list.
with open ("input.txt", "rt") as myfile:    # Open lorem.txt for reading text.
    for myline in myfile:                   # For each line in the file,
        mylines.append(myline.rstrip('\n')) # strip newline and add to list.




for x in range(len(mylines)):
    print (mylines[x])

print (mylines[x])

i = 1

if mylines [i] == ("[Stations]"):
    while(True):
        i+=1 
        Trainstations.append(mylines[i])
        if(Tstring == mylines[i+1]):
            break
i+=2

if mylines [i] == ("[Lines]"): 
    print(i)     
    while(True):
        i+=1 
        Trains.append(mylines[i])
        if(Trainstring == mylines[i+1]):
            break


i+=2

if mylines [i] == ("[Trains]"): 
    print(i)     
    while(True):
        i+=1 
        Trains.append(mylines[i])
        if(Trainstring == mylines[i+1]):
            break










i+=2

if mylines [i] == ("[Passengers]"): 
    print(i)     
    while(True):
        i+=1 
        Passengers.append(mylines[i])
        if(Passengersstring == mylines[i+1]):
            break



print(i) 
    
    
# Strecken: str(ID) str(Anfang) str(Ende) dec(LÃ¤nge) int(KapazitÃ¤t)

    
print(mylines)
