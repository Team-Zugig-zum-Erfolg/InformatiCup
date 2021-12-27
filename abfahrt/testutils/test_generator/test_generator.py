import subprocess, argparse, sys

from abfahrt.Generator import Generator

class test_generator:

    def run(self):

        generator = Generator()
        test_number = 0
        
        parser = argparse.ArgumentParser()
        parser.add_argument('check',type= str, default = "10,60,1000,40,20,10,100,20,100,60,200" ,nargs='?', help="test_amount, size_station, size_lines, size_trains, size_pa, sc_max, lc_max (lc=line capacity), ll_max (ll=line length), tc_max (tc = train capacity), pgs_max (pgs = passenger group size), ptr_max(passenger target round")
        args = parser.parse_args()
               
        if(args.check == "10,60,1000,40,20,10,100,20,100,60,200"):  
            print("Please check documentation for the use of this function and be more creative")
            print("Basic test 10,60,1000,40,20,10,100,20,100,60,200 was used")
        if(args.check != ""):  
            command = args.check.split(',')
               
        if len(command) < 11:
            print("error, to few arguments")
            sys.exit()
        if len(command) > 11:
            print("error, to many arguments")
            sys.exit()


        test_amount = int(command[0])

        for i in range(test_amount):
            test_number += 1
            #random_input_generate_file(size_station, size_lines, size_trains, size_pa, sc_max, lc_max (lc=line capacity), ll_max (ll=line length),
            #                           tc_max (tc = train capacity), pgs_max (pgs = passenger group size), ptr_max(passenger target round))
            
            generator.random_input_generate_file(int(command[1]), int(command[2]), int(command[3]), int(command[4]), int(command[5]), int(command[6]), int(command[7]), int(command[8]), int(command[9]), int(command[10])) 

            p1 = subprocess.run('python -m abfahrt < output_generated.txt', capture_output=True,shell=True)

            if 'error' in p1.stderr.decode("utf-8"):
                print("Error in test: "+str(test_number))
                break
            
            p2 = subprocess.run('"abfahrt/simulator/Bahn-Simulator.exe" -input output_generated.txt -output output.txt -verbose', stdout=subprocess.PIPE, shell=True)

            if('Printing score' in (p2.stdout.decode("utf-8"))):
                print("Successful test: "+str(test_number))
            else:
                print("Error in test: "+str(test_number))
                break

        print("Successful tests: "+str(test_number)+"/"+str(test_amount))

