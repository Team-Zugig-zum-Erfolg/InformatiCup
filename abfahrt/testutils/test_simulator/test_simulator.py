import subprocess
import os
import platform
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
            if platform.system() == "Linux":
                p1 = subprocess.run(
                    'python3 -m abfahrt < abfahrt/testfiles/' + files_test[i], capture_output=True, shell=True)
            elif platform.system() == "Windows":
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
            if platform.system() == "Linux":
                p2 = subprocess.run('"./abfahrt/simulator/bahn-simulator" -input abfahrt/testfiles/' +
                                    files_test[i] + ' -output output.txt -verbose', stdout=subprocess.PIPE, shell=True, cwd=".")
            elif platform.system() == "Windows":
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
