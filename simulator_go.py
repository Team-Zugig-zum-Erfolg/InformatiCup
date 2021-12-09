import subprocess
import sys

result = subprocess.run([sys.executable, "-c", "print('ocean')"])


subprocess.Popen(["rm","-r","some.file"])



print(result)