# The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. This module intends to replace several older modules and functions. (https://docs.python.org/3/library/subprocess.html)
import subprocess

#The argparse module makes it easy to write user-friendly command-line interfaces. The program defines what arguments it requires, and argparse will figure out how to parse those out of sys.argv. The argparse module also automatically generates help and usage messages and issues errors when users give the program invalid arguments. (https://docs.python.org/3/library/argparse.html)
import argparse

#Returns the system/OS name, such as 'Linux', 'Darwin', 'Java', 'Windows'. An empty string is returned if the value cannot be determined. (https://docs.python.org/3/library/platform.html)
from platform import system


from abfahrt.Generator import Generator


class test_generator:

    def run(self):

        generator = Generator()
        test_number = 0
        
        parser = argparse.ArgumentParser()
        parser.add_argument('test_amount',
                            type= int,
                            default = "10",
                            nargs='?',
                            help="Use this Format with Intengers = max_stations, max_lines, max_trains, max_passengers, max_capacity_station, max_capacity_line, max_length_line, max_capacity_train, max_groupsize_passenger, max_targettime_passenger")
        
        parser.add_argument('max_stations',
                            type= int,
                            default = "10",
                            nargs='?')
            
        parser.add_argument('max_lines',
                            type= int,
                            default = "20",
                            nargs='?')  
      
        parser.add_argument('max_trains',
                            type= int,
                            default = "10",
                            nargs='?')                

        parser.add_argument('max_passengers',
                            type= int,
                            default = "10",
                            nargs='?') 

        parser.add_argument('max_capacity_station',
                            type= int,
                            default = "10",
                            nargs='?') 

        parser.add_argument('max_capacity_line',
                            type= int,
                            default = "10",
                            nargs='?') 

        parser.add_argument('max_length_line',
                            type= int,
                            default = "10",
                            nargs='?') 

        parser.add_argument('max_capacity_train',
                            type= int,
                            default = "10",
                            nargs='?') 

        parser.add_argument('max_groupsize_passenger',
                            type= int,
                            default = "10",
                            nargs='?')                            

        parser.add_argument('max_targettime_passenger',
                            type= int,
                            default = "10",
                            nargs='?') 

        args = parser.parse_args()
    
        test_amount = args.test_amount

        for i in range(test_amount):
            test_number += 1
            #random_input_generate_file(size_station, size_lines, size_trains, size_pa, sc_max, lc_max (lc=line capacity), ll_max (ll=line length),
            #                           tc_max (tc = train capacity), pgs_max (pgs = passenger group size), ptr_max(passenger target round))
            
            generator.random_input_generate_file(args.max_stations, args.max_lines, args.max_trains, args.max_passengers, args.max_capacity_station, args.max_capacity_line, args.max_length_line, args.max_capacity_train, args.max_groupsize_passenger, args.max_targettime_passenger)
        
            if system() == "Linux":
                p1 = subprocess.run('python3 -m abfahrt < output_generated.txt', capture_output=True,shell=True)
            
            elif system() == "Windows":
                p1 = subprocess.run('python -m abfahrt < output_generated.txt', capture_output=True,shell=True)
            else:
                return

            if 'error' in p1.stderr.decode("utf-8"):
                print("Error in test: "+str(test_number))
                break
            

            if system() == "Linux":
                p2 = subprocess.run('"./abfahrt/simulator/bahn-simulator" -input output_generated.txt -output output.txt -verbose', stdout=subprocess.PIPE, shell=True)
            
            elif system() == "Windows":
                p2 = subprocess.run('"abfahrt/simulator/Bahn-Simulator.exe" -input output_generated.txt -output output.txt -verbose', stdout=subprocess.PIPE, shell=True)
            else:
                return

            if('Printing score' in (p2.stdout.decode("utf-8"))):
                print("Successful test: "+str(test_number))
            else:
                print("Error in test: "+str(test_number))
                break

        print("Successful tests: "+str(test_number)+"/"+str(test_amount))
