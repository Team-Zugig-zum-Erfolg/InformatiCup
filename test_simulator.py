import subprocess, signal, time, os, io
import pathlib
import sys
import argparse

files_test = os.listdir('test/')
files_test.remove('testlexicon.txt')
files_test.remove('.DS_Store')

files_test.remove('test_100_passengers.txt')

#files_test = ['test_1', 'test_2', 'test_3', 'test_4']

score = 0
Errlist = []

for i in range(len(files_test)):
   
    print('========' + files_test[i] + '========') 
    
    p = subprocess.Popen('python main.py' + ' < test/' + files_test[i], shell = True)
    out, err = p.communicate()

    print('====' + files_test[i] + '++++gotest' '====') 
    
    p = subprocess.run('Bahn-Simulator.exe -input test/' + files_test[i] + ' -output output.txt -verbose', stdout=subprocess.PIPE, shell = True)
    print(p.stdout.decode("utf-8"))
    
    if('Printing score' in (p.stdout.decode("utf-8"))):
        score = score + 1
    else:
        Errlist.append(files_test[i])
        
print('Files tested:')
print(files_test) 
print('\n' + 'Testscore: ' + str(score) + ' from ' + str(len(files_test)) + '\n')

if(score == len(files_test)):
    print("Test was successfully completed")
else:    
    print('List of failed testcases:')
    print('\n'.join(map(str, Errlist)))


















