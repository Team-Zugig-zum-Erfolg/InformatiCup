# The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. This module intends to replace several older modules and functions. (https://docs.python.org/3/library/subprocess.html)
import subprocess

# This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, see the os.path module, and if you want to read all the lines in all the files on the command line see the fileinput module. For creating temporary files and directories see the tempfile module, and for high-level file and directory handling see the shutil module. (https://docs.python.org/3/library/os.html)
import os

#Returns the system/OS name, such as 'Linux', 'Darwin', 'Java', 'Windows'. An empty string is returned if the value cannot be determined. (https://docs.python.org/3/library/platform.html)
from platform import system

# This module provides various time-related functions. For related functionality, see also the datetime and calendar modules. (https://docs.python.org/3/library/time.html)
import time

files_test = os.listdir('abfahrt/testfiles/')
files_test.remove('testlexicon.txt')
files_test.remove('.DS_Store')
files_test.remove('test_100_passengers.txt')


tests_completed = 0
Errlist = []


class test_simulator:

    error_messages = ["Traceback", "Error", "error"]

    def simulator(self):
        global tests_completed
        global Errlist
        for i in range(len(files_test)):
            print('========' + files_test[i] + '========')
            start_time = time.time()
            if system() == "Linux":
                p1 = subprocess.run(
                    'python3 -m abfahrt < abfahrt/testfiles/' + files_test[i], capture_output=True, shell=True)
            elif system() == "Windows":
                p1 = subprocess.run(
                    'python -m abfahrt < abfahrt/testfiles/' + files_test[i], capture_output=True, shell=True)
            else:
                return
            end_time = time.time()
            for error_message in self.error_messages:
                if error_message in p1.stdout.decode("utf-8") or error_message in p1.stderr.decode("utf-8"):
                    Errlist.append(files_test[i])
                    continue
            # print('====' + files_test[i] + '++++gotest' '====')
            if system() == "Linux":
                p2 = subprocess.run('"./abfahrt/simulator/bahn-simulator" -input abfahrt/testfiles/' +
                                    files_test[i] + ' -output output.txt -verbose', stdout=subprocess.PIPE, shell=True, cwd=".")
            elif system() == "Windows":
                p2 = subprocess.run('"abfahrt/simulator/bahn-simulator.exe" -input abfahrt/testfiles/' +
                                    files_test[i] + ' -output output.txt -verbose', stdout=subprocess.PIPE, shell=True, cwd=".")
            else:
                return
            # print(p2.stdout.decode("utf-8"))

            if('Printing score' in (p2.stdout.decode("utf-8"))):
                found = False
                current_score = "0"
                for line in (p2.stdout.decode("utf-8").splitlines()):
                    if found == True:
                        current_score = line
                        break
                    if line == 'Printing score':
                        found = True
                print("Score: "+current_score)
                print("Time: "+str(round(((end_time-start_time)/60), 4))+" min")
                tests_completed += 1
            else:
                Errlist.append(files_test[i])

        print('\nFiles tested:')
        print(files_test)
        print('\n' + 'Files/Testcases successfully tested: ' + str(tests_completed) +
              ' of ' + str(len(files_test)) + '\n')

        if(tests_completed == len(files_test)):
            print("Test was successfully completed")
        else:
            print('List of failed testcases:')
            print('\n'.join(map(str, Errlist)))
