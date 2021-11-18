const_start = 0
const_end = 1
const_train_Id = 2
const_lineId = 0
const_station_1 = 1
const_station_2 = 2
const_length = 3
const_capacity = 4

#Beispiel from linelist
linelist = [[1 ,1 ,2 ,4.62768 ,2 ], [2 ,2 ,3 ,4.94065 ,1], [3, 1, 3, 4.92471, 2]] #[a,c,d,e,b] a->Line_Id, b->capacity 

#----initial-----
Line = []
Line.append(None) #L0 -> None
i = 1
for list in linelist:
    Line.append([])
    for capacity in range(list[const_capacity]):
        Line[i].append([])
    i = i + 1
#----initial-----
print(Line)#[None, [[], []], [[]], [[], []]]

# Beispiel [int start, int end, int train_Id]
train_in_line1 = [4, 6, 1]
train_in_line2 = [7, 9, 2]
train_in_line3 = [10, 13, 3]

#train_in_line put in capacity
Line[1][0].append(train_in_line1)
Line[1][0].append(train_in_line2)
Line[1][0].append(train_in_line3)

for line in Line:
    if line != None:
        print(line)
        for capacity in line:
            print(capacity)
            for train_in_line in capacity:
                print(train_in_line)
                print("Start:"+ str(train_in_line[const_start]))
                print("end:" + str(train_in_line[const_end]))
                print("train:" + str(train_in_line[const_train_Id]))
