# The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. This module intends to replace several older modules and functions. (https://docs.python.org/3/library/subprocess.html)
import subprocess

# The argparse module makes it easy to write user-friendly command-line interfaces. The program defines what arguments it requires, and argparse will figure out how to parse those out of sys.argv. The argparse module also automatically generates help and usage messages and issues errors when users give the program invalid arguments. (https://docs.python.org/3/library/argparse.html)
import argparse

# This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, see the os.path module, and if you want to read all the lines in all the files on the command line see the fileinput module. For creating temporary files and directories see the tempfile module, and for high-level file and directory handling see the shutil module. (https://docs.python.org/3/library/os.html)
import os

# Returns the system/OS name, such as 'Linux', 'Darwin', 'Java', 'Windows'. An empty string is returned if the value cannot be determined. (https://docs.python.org/3/library/platform.html)
from platform import system

# This module provides various time-related functions. For related functionality, see also the datetime and calendar modules. (https://docs.python.org/3/library/time.html)
import time


ERRORS_MESSAGES = ["Traceback", "Error", "error"]


class test_simulator:

    def __init__(self, dir: str):
        self.files_test = os.listdir(dir)
        self.files_test.remove('testlexicon.txt')
        self.dir = dir

        self.tests_completed = 0
        self.Errlist = []

    def run(self):

        parser = argparse.ArgumentParser(
            description="Simulator zum automatischen Testen unserer Software", add_help=False)

        parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                            help='Zeigt dieses Hilfemenü an')
        parser.add_argument('-verbose',
                            action='store_true',
                            help="Zeigt die vollständige Ausgabe an")
        parser.add_argument('-singletest',
                            type=str,
                            metavar='[file]',
                            help="Führt nur einen Test mit dieser Eingabedatei aus")
        parser.add_argument('-soft',
                            action='store_true',
                            help="Stoppt das Testen bei einem Fehler")

        args = parser.parse_args()

        if args.singletest and args.singletest in self.files_test:
            self.files_test = [args.singletest]
        elif args.singletest:
            print("Eingabedatei existiert nicht!")
            return

        for i in range(len(self.files_test)):
            error = False
            print('========' + self.files_test[i] + '========')
            start_time = time.time()
            if system() == "Linux":
                p1 = subprocess.run(
                    'python3 -m abfahrt < ' + self.dir + '/' + self.files_test[i], capture_output=True, shell=True)
            elif system() == "Windows":
                p1 = subprocess.run(
                    'python -m abfahrt < ' + self.dir + '/' + self.files_test[i], capture_output=True, shell=True)
            else:
                return
            end_time = time.time()

            if args.verbose:
                print(p1.stdout.decode("utf-8"))

            for error_message in ERRORS_MESSAGES:
                if error_message in p1.stdout.decode("utf-8") or error_message in p1.stderr.decode("utf-8"):
                    print("Fehler")
                    self.Errlist.append(self.files_test[i])
                    error = True
                    break
            if error:
                if args.soft:
                    break
                continue

            if system() == "Linux":
                p2 = subprocess.run('"./abfahrt/simulator/bahn-simulator" -input abfahrt/testfiles/' +
                                    self.files_test[i] + ' -output output.txt -verbose', stdout=subprocess.PIPE, shell=True, cwd=".")
            elif system() == "Windows":
                p2 = subprocess.run('"abfahrt/simulator/bahn-simulator.exe" -input abfahrt/testfiles/' +
                                    self.files_test[i] + ' -output output.txt -verbose', stdout=subprocess.PIPE, shell=True, cwd=".")
            else:
                return

            if args.verbose:
                print(p2.stdout.decode("utf-8"))

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
                print("Zeit: "+str(round(((end_time-start_time)/60), 4))+" min")
                self.tests_completed += 1
            else:
                print("Fehler")
                self.Errlist.append(self.files_test[i])
                if args.soft:
                    break

        print('\nGetestete Dateien:')
        print(self.files_test)
        print('\n' + 'Dateien/Testfälle die erfolgreich getestet wurden: ' + str(self.tests_completed) +
              ' von ' + str(len(self.files_test)) + '\n')

        if(self.tests_completed == len(self.files_test)):
            print("Tests wurden erfolgreich durchgeführt")
        else:
            print('Folgende Tests schlugen fehl:')
            print('\n'.join(map(str, self.Errlist)))
