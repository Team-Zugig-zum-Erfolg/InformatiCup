import subprocess, signal, time, os
import pathlib
import sys
import argparse

#csp = str(pathlib.Path(__file__).parent.resolve()) 
#csp = csp[:-1]
#csp = csp + 'g'
#print(csp)

files_test = os.listdir('test/')
files_test.remove('testlexicon.txt')
files_test.remove('.DS_Store')
#files_test = ['test_1','test_2','test_3','test_4']

print(files_test) 

for i in range(len(files_test)):
   
    print('========' + files_test[i] + '========') 
    
    p = subprocess.Popen('python main.py' + ' ' + files_test[i], shell = True)
    out, err = p.communicate()

    print('====' + files_test[i] + '++++gotest' '====') 
    
    p = subprocess.run('Bahn-Simulator.exe -input test/' + files_test[i] + ' -output output.txt -verbose', shell = True)

print("end")
print(files_test) 
