import signal
import subprocess
import subprocess, signal, time
import pathlib
import sys
import argparse

#csp = str(pathlib.Path(__file__).parent.resolve()) 
#csp = csp[:-1]
#csp = csp + 'g'
#print(csp)

list = ['test_1','test_2','test_3','test_4']


for i in range(len(list)):
   
    print('======================================' + list[i] + '===========================================') 
    
    p = subprocess.Popen('python main.py' + ' ' + list[i] + '.txt', shell = True)
    out, err = p.communicate()



for j in range(len(list)):
    
    print('======================================' + list[j] + '_gotest' '===========================================') 
    
    p = subprocess.run('Bahn-Simulator.exe -input test/' + list[j] + '.txt -output output.txt -verbose', shell = True)


print("end")

