import subprocess
import sys
import os

result = subprocess.run([sys.executable, "-c", "print('ocean')"])


#subprocess.Popen(["rm","-r","some.file"])


os.spawnl(os.P_DETACH, 'main.py')

print(result)