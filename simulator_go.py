import os
import signal
import subprocess
import subprocess, signal, time

p = subprocess.Popen('python main.py test_1', shell = True)

out, err = p.communicate()
print(err)
print(out)

p.terminate()

#time.sleep(3) #Wait 5 secs before killing
#p.send_signal(signal.CTRL_C_EVENT)



p = subprocess.Popen('Bahn-Simulator.exe -input input.txt -output output.txt -verbose', shell = True)

out, err = p.comunicate()
print(err)
print(out)


print("gggg")

