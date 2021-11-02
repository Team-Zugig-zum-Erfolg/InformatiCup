num =       ("#Kommentar"+ 
             "#Leere Zeilen werden Ignoriert \n" + 
             "#str: ([a-z] | [A-Z] | [0-9] | _ \n)+" +
             "#dec: Dezimahlzahl mit beliebig vielen Nachkommastellen \n" +
             "#int: Ganzahle mit beliebig vielen Stellen >=0 \n" +
             "#Werte-Trenner: 0x20 (SPACE) \n" +
             "#Zeilen-Trenner: 0x0A (NEWLINE) \n")
print(num)

  



mylines = []                                # Declare an empty list.
with open ("input.txt", "rt") as myfile:    # Open lorem.txt for reading text.
    for myline in myfile:                   # For each line in the file,
        mylines.append(myline.rstrip('\n')) # strip newline and add to list.



    print(mylines)
