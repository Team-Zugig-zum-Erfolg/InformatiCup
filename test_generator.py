import subprocess

from Generator import Generator

generator = Generator()

class test_generator:

    def simulator(self):

        generator = Generator()
        score = 0
        tests = 10

        for i in range(tests):
            generator.random_input_generate_file(40,300,10,20,10,4,20,100,60,200)
            p = subprocess.Popen('python main.py' +
                                 ' < output_generated.txt', shell=True)
            out, err = p.communicate()
            p = subprocess.run('Bahn-Simulator.exe -input output_generated.txt -output output.txt -verbose', stdout=subprocess.PIPE, shell=True)
            print(p.stdout.decode("utf-8"))

            if('Printing score' in (p.stdout.decode("utf-8"))):
                score += 1
            elif 'Error: Capacity of all trains to low!' in p.stdout.decode("utf-8") or 'Error: Too many trains in station at beginning!' in p.stdout.decode("utf-8"):
                print("Skipped")
                score += 1
                break
            else:
                print("Error")
                break

        print(str(score)+"/"+str(tests))


ts = test_generator()
ts.simulator()
