import subprocess

from Generator import Generator

generator = Generator()

class test_generator:

    def simulator(self):

        generator = Generator()
        score = 0
        tests = 10

        for i in range(tests):
            generator.random_input_generate_file(60,1000,10,20,10,100,20,100,60,200) 
            p1 = subprocess.run('python main.py < output_generated.txt', capture_output=True,shell=True)

            if 'Too many trains in station at beginning' in p1.stderr.decode("utf-8"):
                print("Skipped (because input is not valid (too many trains at station at beginning))")
                score += 1
                continue
            
            p2 = subprocess.run('Bahn-Simulator.exe -input output_generated.txt -output output.txt -verbose', stdout=subprocess.PIPE, shell=True)
            #print(p.stdout.decode("utf-8"))

            if('Printing score' in (p2.stdout.decode("utf-8"))):
                score += 1
                print("Successful: "+str(score))
            else:
                print("Error")
                break

        print(str(score)+"/"+str(tests))


ts = test_generator()
ts.simulator()