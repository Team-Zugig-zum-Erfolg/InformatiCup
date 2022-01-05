# Team zug zum erfolg

Team Arbeit Informati Cup

main:

python -m abfahrt [< input.txt]

Example:
python -m abfahrt < abfahrt/testfiles/test_1.txt


test_simulator:

python -m abfahrt.testutils.test_simulator

Example only one Test:

python -m abfahrt.testutils.test_simulator -singletest test_1.txt

Example Verbose:

python -m abfahrt.testutils.test_simulator -verbose

Example soft:

python -m abfahrt.testutils.test_simulator -soft

test_generator:

python -m abfahrt.testutils.test_generator

Example:
python -m abfahrt.testutils.test_generator


python -m abfahrt.testutils.test_generator -test_amount 10 -number_stations 10 -number_lines 20 -number_trains 10 -number_passengers 10 -max_capacity_station 10 -max_capacity_line 10 -max_length_line 10 -max_capacity_train 10 -max_groupsize_passenger 10 -max_targettime_passenger 10 -max_speed_train 10