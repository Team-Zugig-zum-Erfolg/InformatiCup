import subprocess
import os

files_test = os.listdir('abfahrt/testfiles/')
files_test.remove('testlexicon.txt')
files_test.remove('.DS_Store')
files_test.remove('test_100_passengers.txt')


score = 0
Errlist = []


class test_simulator:

    def simulator(self):
        global score
        global Errlist
        for i in range(len(files_test)):
            print('========' + files_test[i] + '========')
            p = subprocess.Popen('python -m abfahrt < abfahrt/testfiles/' + files_test[i], shell=True)
            out, err = p.communicate()
            print('====' + files_test[i] + '++++gotest' '====')
            p = subprocess.run('"abfahrt/simulator/Bahn-Simulator.exe" -input abfahrt/testfiles/' +
                               files_test[i] + ' -output output.txt -verbose', stdout=subprocess.PIPE, shell=True, cwd=".")
            print(p.stdout.decode("utf-8"))

            if('Printing score' in (p.stdout.decode("utf-8"))):
                score += 1
            else:
                Errlist.append(files_test[i])

        print('Files tested:')
        print(files_test)
        print('\n' + 'Testscore: ' + str(score) +
              ' from ' + str(len(files_test)) + '\n')

        if(score == len(files_test)):
            print("Test was successfully completed")
        else:
            print('List of failed testcases:')
            print('\n'.join(map(str, Errlist)))


