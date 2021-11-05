Trainstations = []  
Lines = []
Trains = []
Passengers = []
i = 0

mylines = []                                # Declare an empty list.
with open ("input.txt", "rt") as myfile:    # Open lorem.txt for reading text.
    for myline in myfile:                   # For each line in the file,
        mylines.append(myline.rstrip('\n')) # strip newline and add to list.

mylines.append("")

while(True):

    if mylines [i] == ("[Stations]"):
        while(True):
            i+=1 
            Trainstations.append(mylines[i])
            if(('#' in mylines[i+1]) or ("" == mylines[i+1])):
                break

    if mylines [i] == ("[Lines]"): 
        print(i)     
        while(True):
            i+=1 
            Lines.append(mylines[i])
            if(('#' in mylines[i+1]) or ("" == mylines[i+1])):
                break


    if mylines [i] == ("[Trains]"): 
        print(i)     
        while(True):
            i+=1 
            Trains.append(mylines[i])
            if(('#' in mylines[i+1]) or ("" == mylines[i+1])):
                break


    if mylines [i] == ("[Passengers]"):      
        while(True):
            i+=1 
            Passengers.append(mylines[i])
            if(('#' in mylines[i+1]) or ("" == mylines[i+1])):
                break    
        break
    
    i+=1
print(i)

