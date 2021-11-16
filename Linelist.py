const_start = 0
const_end = 1
const_train_Id = 2

Linelist = [[1,2], [2,1], [3,2]] #[1,2] a->L1, b->capacity Beispiel

Line = []
Line.append(None)
i = 1
for list in Linelist:
    Line.append([])
    for capacity in range(list[1]):
        Line[i].append([])
    i = i + 1

print(Line)

# [int start, int end, int train_Id] 
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
