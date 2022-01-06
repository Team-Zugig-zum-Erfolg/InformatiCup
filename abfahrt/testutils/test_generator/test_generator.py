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
        test_number = 1
        test_success = 0
        
        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS,
                formatter_class=lambda prog: argparse.HelpFormatter(
                    prog, max_help_position=80, width=130), description="Generator der automatisch Tests für unsere Software erstellt und testet", add_help=False)


        parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                            help='Zeigt dieses Hilfemenü an')
        
        parser.add_argument('-test_amount',
                            type= int,
                            default = "10", 
                            metavar='[int]',                        
                            help="Anzahl der auszuführenden Tests")

        parser.add_argument('-number_stations',
                            type= int,
                            default = "10",
                            metavar='[int]',
                            help="Anzahl an Bahnhöfen")
            
        parser.add_argument('-number_lines',
                            type= int,
                            default = "20",
                            metavar='[int]',
                            help="Anzahl an Strecken")  
      
        parser.add_argument('-number_trains',
                            type= int,
                            default = "10",
                            metavar='[int]',
                            help="Anzahl an Zügen")                

        parser.add_argument('-number_passengers',
                            type= int,
                            default = "10",
                            metavar='[int]',
                            help="Anzahl an Passagieren")

        parser.add_argument('-max_capacity_station',
                            type= int,
                            default = "10",
                            metavar='[int]',
                            help="Maximale Kapazität von einem Bahnhof") 

        parser.add_argument('-max_capacity_line',
                            type= int,
                            default = "10",
                            metavar='[int]',
                            help="Maximale Kapazität von einer Strecke")

        parser.add_argument('-max_length_line',
                            type= int,
                            default = "10",
                            metavar='[int]',
                            help="Maximale Länge von einer Strecke")

        parser.add_argument('-max_capacity_train',
                            type= int,
                            default = "10",
                            metavar='[int]',
                            help="Maximale Kapazität von einem Zug")

        parser.add_argument('-max_groupsize_passenger',
                            type= int,
                            default = "10",
                            metavar='[int]',
                            help="Maximale Gruppengröße bei einem Passagier")                          

        parser.add_argument('-max_targettime_passenger',
                            type= int,
                            default = "10",
                            metavar='[int]',
                            help="Maximale Zielzeit bzw. -runde bei einem Passagier")

        parser.add_argument('-max_speed_train',
                            type= int,
                            default = "10",
                            metavar='[int]',
                            help="Maximale Geschwindigkeit von einem Zug")

        parser.add_argument('-verbose',
                            action='store_true',
                            help="Zeigt die vollständige Ausgabe an")

        parser.add_argument('-soft',
                            action='store_true',
                            help="Stoppt das Testen bei einem Fehler")


        args = parser.parse_args()
    
        for i in range(args.test_amount):
            
            generator.random_input_generate_file(args.number_stations, args.number_lines, args.number_trains, args.number_passengers, args.max_capacity_station, args.max_capacity_line, args.max_length_line, args.max_capacity_train, args.max_groupsize_passenger, args.max_targettime_passenger, args.max_speed_train)
        
            if system() == "Linux":
                p1 = subprocess.run('python3 -m abfahrt < output_generated.txt', capture_output=True,shell=True)
            
            elif system() == "Windows":
                p1 = subprocess.run('python -m abfahrt < output_generated.txt', capture_output=True,shell=True)
            else:
                return

            if args.verbose:
                print(p1.stdout.decode("utf-8"))


            if 'error' in p1.stderr.decode("utf-8"):
                print("Error in test: "+str(test_number))
                if args.soft:
                    break

            if system() == "Linux":
                p2 = subprocess.run('"./abfahrt/simulator/bahn-simulator" -input output_generated.txt -output output.txt -verbose', stdout=subprocess.PIPE, shell=True)
            
            elif system() == "Windows":
                p2 = subprocess.run('"abfahrt/simulator/Bahn-Simulator.exe" -input output_generated.txt -output output.txt -verbose', stdout=subprocess.PIPE, shell=True)
            else:
                return
            if args.verbose:
                print(p2.stdout.decode("utf-8"))

            if('Printing score' in (p2.stdout.decode("utf-8"))):
                test_success += 1
                print("Successful test: "+str(test_number))
            else:
                print("Error in test: "+str(test_number))
                if args.soft:
                    break
            test_number += 1

        print("Successful tests: "+str(test_success)+"/"+str(args.test_amount))
