import subprocess

from Generator import Generator

generator = Generator()

class test_generator:

    def simulator(self):

        generator = Generator()
        test_number = 0
        test_amount = 10

        for i in range(test_amount):
            test_number += 1
            generator.random_input_generate_file(60,1000,10,20,10,100,20,100,60,200) 
            p1 = subprocess.run('python main.py < output_generated.txt', capture_output=True,shell=True)

            if 'Too many trains in station at beginning' in p1.stderr.decode("utf-8"):
                print("Skipped (because input is not valid (too many trains at station at beginning))")
                continue
            
            p2 = subprocess.run('Bahn-Simulator.exe -input output_generated.txt -output output.txt -verbose', stdout=subprocess.PIPE, shell=True)

            if('Printing score' in (p2.stdout.decode("utf-8"))):
                print("Successful test: "+str(test_number))
            else:
                print("Error in test: "+str(test_number))
                break

        print("Successful tests: "+str(test_number)+"/"+str(test_amount))


ts = test_generator()
ts.simulator()