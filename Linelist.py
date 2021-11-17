const_start = 0
const_end = 1
const_train_Id = 2
#Beispiel from linelist
linelist = [[1 ,1 ,2 ,4.62768 ,2 ], [2 ,2 ,3 ,4.94065 ,1], [3, 1, 3, 4.92471, 2]] #[a,c,d,e,b] a->L1, b->capacity 

#----initial-----
Line = []
Line.append(None)
i = 1
for list in linelist:
    Line.append([])
    for capacity in range(list[4]):
        Line[i].append([])
    i = i + 1
#----initial-----
print(Line)#[None, [[], []], [[]], [[], []]]

# Beispiel [int start, int end, int train_Id] 
train_in_line = [2, 4, 1]
train_in_line1 = [6, 8, 1]
train_in_line2 = [10, 12, 1]

Line[1][0].append(train_in_line)
Line[1][0].append(train_in_line1)
Line[1][0].append(train_in_line2)

print(Line)
for line in Line:
    if line != None:
        for capacity in line:
            for time in capacity:
                print("Start:"+ str(time[const_start]))
                print("end:" + str(time[const_end]))
                print("train:" + str(time[const_train_Id]))
