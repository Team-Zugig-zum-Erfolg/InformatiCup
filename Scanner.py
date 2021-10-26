num = input ("#Kommentar"+ 
             "#Leere Zeilen werden Ignoriert \n" + 
             "#str: ([a-z] | [A-Z] | [0-9] | _ \n)+" +
             "#dec: Dezimahlzahl mit beliebig vielen Nachkommastellen \n" +
             "#int: Ganzahle mit beliebig vielen Stellen >=0 \n" +
             "#Werte-Trenner: 0x20 (SPACE) \n" +
             "#Zeilen-Trenner: 0x0A (NEWLINE) \n")
print(num)
name1 = input("Enter name : ")
print(name1)
  
# Printing type of input value
print ("type of number", type(num))
print ("type of name", type(name1))