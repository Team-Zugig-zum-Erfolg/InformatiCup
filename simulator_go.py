import signal
import subprocess
import subprocess, signal, time
import pathlib

#csp = str(pathlib.Path(__file__).parent.resolve()) 
#csp = csp[:-1]
#csp = csp + 'g'
#print(csp)


p = subprocess.Popen('python main.py test_1', shell = True)
out, err = p.communicate()


p = subprocess.run('Bahn-Simulator.exe -input input.txt -output output.txt -verbose', shell = True)


print("end")

