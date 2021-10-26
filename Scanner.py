num = input ("#Kommentar"+ 
             "#Leere Zeilen werden Ignoriert" + 
             "#str: ([a-z] | [A-Z] | [0-9] | _)+" +
             "#dec: Dezimahlzahl mit beliebig vielen Nachkommastellen" +
             "#int: Ganzahle mit beliebig vielen Stellen >=0" +
             "#Werte-Trenner: 0x20 (SPACE)" +
             "#Zeilen-Trenner: 0x0A (NEWLINE)")
print(num)
name1 = input("Enter name : ")
print(name1)
  
# Printing type of input value
print ("type of number", type(num))
print ("type of name", type(name1))