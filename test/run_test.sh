#!/bin/bash

TESTRESULT="results"

if [[ -f $TESTRESULT ]]; then
	rm $TESTRESULT
fi
RESULT="PASS"


TEST="==TEST 1: TESTING FIRST MODE WIHTOUT MODIFIED MODE PATH=="
TESTOUT="test1.out"
TESTLOG="test1.log"
if [[ -f "logs/$TESTLOG" ]]; then
	rm "logs/$TESTLOG"
fi
if [[ -f "logs/$TESTOUT" ]]; then
	rm "logs/$TESTOUT"
fi

echo $TEST | tee -a $TESTRESULT
echo -ne '\n\n\n1' | python3 ../src/treerun/main.py -c input.yaml -l "logs/$TESTLOG" >> "logs/$TESTOUT"

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" "logs/$TESTOUT") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some files could not be located:" >> $TESTRESULT
if [ $(grep -c "Unable to locate\|" "logs/$TESTOUT") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Not found\|Unsuccessful*" "logs/$TESTLOG") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo >> $TESTRESULT


TEST="==TEST 2: TESTING SECOND MODE WITH MODIFIED MODE PATH (test-1)=="
TESTOUT="test2.out"
TESTLOG="test2.log"
rm "logs/$TESTLOG" "logs/$TESTOUT"

echo $TEST | tee -a $TESTRESULT
echo -ne '\n\n\n2' | python3 ../src/treerun/main.py -m 1 -c input.yaml -l "logs/$TESTLOG" >> "logs/$TESTOUT"

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" "logs/$TESTOUT") -eq 1 ]; then
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo "Checking if some files could not be located:" >> $TESTRESULT
if [ $(grep -c "Unable to locate\|" "logs/$TESTOUT") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Not found\|Unsuccessful*" "logs/$TESTLOG") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo >> $TESTRESULT






TEST="==TEST 3: TESTING SECOND MODE WITH MODIFIED MODE PATH (test-SOME_MODIFIER)=="
TESTOUT="test3.out"
TESTLOG="test3.log"
rm "logs/$TESTLOG" "logs/$TESTOUT"

echo $TEST | tee -a $TESTRESULT
echo -ne '\n\n\n2\ny' | python3 ../src/treerun/main.py -m SOME_MODIFIER -c input.yaml -l "logs/$TESTLOG" >> "logs/$TESTOUT"

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" "logs/$TESTOUT") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo "Checking if at least one file could be located:" >> $TESTRESULT
if [ $(grep -c "Do you still want to continue" "logs/$TESTOUT") -eq 1 ]; then
	echo 'PASS' >> $TESTRESULT
else
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Successful*" "logs/$TESTLOG") -eq 1 ]; then
	echo 'PASS' >> $TESTRESULT
else
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
fi
echo >> $TESTRESULT




TEST="==TEST 4: TESTING THIRD MODE WITH MODIFIED MODE PATH (test-1/x)=="
TESTOUT="test4.out"
TESTLOG="test4.log"
rm "logs/$TESTLOG" "logs/$TESTOUT"

echo $TEST | tee -a $TESTRESULT
echo -ne '\n\n\n3\ny' | python3 ../src/treerun/main.py -m 1 -c input.yaml -l "logs/$TESTLOG" >> "logs/$TESTOUT"

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" "logs/$TESTOUT") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo "Checking if some files could not be located:" >> $TESTRESULT
if [ $(grep -c "Do you still want to continue" "logs/$TESTOUT") -eq 1 ]; then
	echo 'PASS' >> $TESTRESULT
else
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Successful*" "logs/$TESTLOG") -eq 1 ]; then
	echo 'PASS' >> $TESTRESULT
else
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
fi
echo >> $TESTRESULT




TEST="==TEST 5: TESTING FIRST MODE WIHTOUT MODIFIED MODE PATH, SELECTING 1:ALL:3=="
TESTOUT="test5.out"
TESTLOG="test5.log"
rm "logs/$TESTLOG" "logs/$TESTOUT"

echo $TEST | tee -a $TESTRESULT
echo -ne '1\n\n3\n1' | python3 ../src/treerun/main.py -c input.yaml -l "logs/$TESTLOG" >> "logs/$TESTOUT"

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" "logs/$TESTOUT") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some files could not be located:" >> $TESTRESULT
if [ $(grep -c "Unable to locate\|" "logs/$TESTOUT") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Not found\|Unsuccessful*" "logs/$TESTLOG") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo >> $TESTRESULT




TEST="==TEST 6: TESTING SECOND MODE WITH MODIFIED MODE PATH (test-1), SELECTING 1:ALL:3=="
TESTOUT="test6.out"
TESTLOG="test6.log"
rm "logs/$TESTLOG" "logs/$TESTOUT"

echo $TEST | tee -a $TESTRESULT
echo -ne '1\n\n3\n2' | python3 ../src/treerun/main.py -m 1 -c input.yaml -l "logs/$TESTLOG" >> "logs/$TESTOUT"

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" "logs/$TESTOUT") -eq 1 ]; then
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo "Checking if some files could not be located:" >> $TESTRESULT
if [ $(grep -c "Unable to locate\|" "logs/$TESTOUT") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Not found\|Unsuccessful*" "logs/$TESTLOG") -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo >> $TESTRESULT



echo "OVERALL RESULT: $RESULT" | tee -a $TESTRESULT
