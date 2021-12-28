import subprocess, argparse, sys

from abfahrt.Generator import Generator

class test_generator:

    def run(self):

        generator = Generator()
        test_number = 0
        
        parser = argparse.ArgumentParser()
        parser.add_argument('input',type= str, default = "" ,nargs='?', help="Use this Format with Intengers = test amount, size stations, size lines, size_trains, size passengers, station capacity max, line capacity max, line length max, train capacity max, passenger group size max, passenger target round")
        args = parser.parse_args()

        if(args.input == ""):
            print("use --help for more informations or check documentation")
            sys.exit()

        if(args.input != ""):  
            command = args.input.split(',')
                            
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

