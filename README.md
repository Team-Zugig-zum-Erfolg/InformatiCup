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
python -m abfahrt.testutils.test_generator 10,60,1000,40,20,10,100,20,100,60,200