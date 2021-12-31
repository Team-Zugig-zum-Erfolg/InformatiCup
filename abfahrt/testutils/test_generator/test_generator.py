import subprocess, argparse, platform

from abfahrt.Generator import Generator

class test_generator:
    """ """

    def run(self):
        """ """

        generator = Generator()
        test_number = 0
        
        parser = argparse.ArgumentParser()
        parser.add_argument('test_amount',
                            type= int,
                            default = "",
                            nargs='?',
                            help="Use this Format with Intengers = test amount size stations size lines size trains size passengers station capacity max line capacity max line length max train capacity max passenger group size max passenger target round")
        
        parser.add_argument('size_stations',
                            type= int,
                            default = "",
                            nargs='?')
            
        parser.add_argument('size_lines',
                            type= int,
                            default = "",
                            nargs='?')  
      
        parser.add_argument('size_trains',
                            type= int,
                            default = "",
                            nargs='?')                

        parser.add_argument('size_passengers',
                            type= int,
                            default = "",
                            nargs='?') 

        parser.add_argument('station_capacity_max',
                            type= int,
                            default = "",
                            nargs='?') 

        parser.add_argument('line_capacity_max',
                            type= int,
                            default = "",
                            nargs='?') 

        parser.add_argument('line_length_max',
                            type= int,
                            default = "",
                            nargs='?') 

        parser.add_argument('train_capacity_max',
                            type= int,
                            default = "",
                            nargs='?') 

        parser.add_argument('passenger_group_size_max',
                            type= int,
                            default = "",
                            nargs='?')                            

        parser.add_argument('passenger_target_round',
                            type= int,
                            default = "",
                            nargs='?') 

        args = parser.parse_args()
    
     #  if(args.input == ""):
     #       print("use --help for more informations or check documentation")
     #       sys.exit()

   #     if(args.input != ""):  
   #         command = args.input.split(',')
                            
    #    if len(command) < 11:
    #        print("error, to few arguments")
    #        sys.exit()
   #     if len(command) > 11:
    #        print("error, to many arguments")
    #        sys.exit()

        test_amount = args.test_amount

        for i in range(test_amount):
            test_number += 1
            #random_input_generate_file(size_station, size_lines, size_trains, size_pa, sc_max, lc_max (lc=line capacity), ll_max (ll=line length),
            #                           tc_max (tc = train capacity), pgs_max (pgs = passenger group size), ptr_max(passenger target round))
            
            generator.random_input_generate_file(args.size_stations, args.size_lines, args.size_trains, args.size_passengers, args.station_capacity_max, args.line_capacity_max, args.line_length_max, args.train_capacity_max, args.passenger_group_size_max, args.passenger_target_round)
        
            if platform.system() == "Linux":
                p1 = subprocess.run('python3 -m abfahrt < output_generated.txt', capture_output=True,shell=True)
            
            elif platform.system() == "Windows":
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

