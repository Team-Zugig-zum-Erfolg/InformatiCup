import sys, glob, re, random

def main():
    original_stdout = sys.stdout # Save a reference to the original standard output
    with open('random_train_test.txt', 'w') as f:
        sys.stdout = f
        print("[Stations]")
        ran_station = (random.randint(2,9))
        for i in range(ran_station):
            print("S"+repr(i+1)+" "+ repr(random.randint(1,9)))
            
        print("\n[Lines]")
        ran_lines = ran_station + (random.randint(1,5))
        
        for i in range(ran_lines):
            ran_station_start = random.randint(1,ran_station-1)     
            ran_station_end = random.randint(1,ran_station)
            
            if ran_station_start == ran_station_end: 
                ran_station_end = ran_station - 1
            print("L"+repr(i+1) +" "+ "S"+repr(ran_station_start) +" "+ "S"+repr(ran_station_end) +" "+ repr(round(random.uniform(0.5, 8.5), 5)) +" "+ repr(random.randint(1,3)))

        print("\n[Trains]")
        ran_train = (random.randint(1,4))
        for i in range(ran_train):
            print("T"+repr(i+1)+" "+  "S"+ repr(random.randint(2,9))    +" "+ repr(round(random.uniform(0.5, 10), 5)) +" "+ repr(random.randint(2,9)))
        
        print("\n[Passengers]")

        for i in range(ran_train + ran_train+ ran_train):
            print("P"+repr(i+1)+" "+  "S"+ repr(random.randint(2,9)) +" "+  "S"+ repr(random.randint(2,9))    +" "+  repr(random.randint(2,9))    +" "+   repr(random.randint(1,80)))
        sys.stdout = original_stdout # Reset the standard output to its original value    
main()
        
        
    

