#!/bin/bash

TESTRESULT="results"

if [[ -f $TESTRESULT ]]; then
	rm $TESTRESULT
fi
RESULT="PASS"


TEST="==TEST 1: TESTING FIRST MODE WIHTOUT MODIFIED MODE PATH=="
TESTOUT="test1.out"
TESTLOG="test1.log"
if [[ -f $TESTLOG ]]; then
	rm $TESTLOG
fi
if [[ -f $TESTOUT ]]; then
	rm $TESTOUT
fi

echo $TEST | tee -a $TESTRESULT
echo -ne '\n\n\n1' | python3 ../treesub.py -c input.yaml -l $TESTLOG >> $TESTOUT

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" $TESTOUT) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some files could not be located:" >> $TESTRESULT
if [ $(grep -c "Unable to locate\|" $TESTOUT) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Not found\|Unsuccessful*" $TESTLOG) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo >> $TESTRESULT


TEST="==TEST 2: TESTING SECOND MODE WITH MODIFIED MODE PATH (test-1)=="
TESTOUT="test2.out"
TESTLOG="test2.log"
rm $TESTLOG $TESTOUT

echo $TEST | tee -a $TESTRESULT
echo -ne '\n\n\n2' | python3 ../treesub.py -m 1 -c input.yaml -l $TESTLOG >> $TESTOUT

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" $TESTOUT) -eq 1 ]; then
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo "Checking if some files could not be located:" >> $TESTRESULT
if [ $(grep -c "Unable to locate\|" $TESTOUT) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Not found\|Unsuccessful*" $TESTLOG) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo >> $TESTRESULT






TEST="==TEST 3: TESTING SECOND MODE WITH MODIFIED MODE PATH (test-SOME_MODIFIER)=="
TESTOUT="test3.out"
TESTLOG="test3.log"
rm $TESTLOG $TESTOUT

echo $TEST | tee -a $TESTRESULT
echo -ne '\n\n\n2\ny' | python3 ../treesub.py -m SOME_MODIFIER -c input.yaml -l $TESTLOG >> $TESTOUT

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" $TESTOUT) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo "Checking if at least one file could be located:" >> $TESTRESULT
if [ $(grep -c "Do you still want to continue" $TESTOUT) -eq 1 ]; then
	echo 'PASS' >> $TESTRESULT
else
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Successful*" $TESTLOG) -eq 1 ]; then
	echo 'PASS' >> $TESTRESULT
else
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
fi
echo >> $TESTRESULT




TEST="==TEST 4: TESTING THIRD MODE WITH MODIFIED MODE PATH (test-1/x)=="
TESTOUT="test4.out"
TESTLOG="test4.log"
rm $TESTLOG $TESTOUT

echo $TEST | tee -a $TESTRESULT
echo -ne '\n\n\n3\ny' | python3 ../treesub.py -m 1 -c input.yaml -l $TESTLOG >> $TESTOUT

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" $TESTOUT) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo "Checking if some files could not be located:" >> $TESTRESULT
if [ $(grep -c "Do you still want to continue" $TESTOUT) -eq 1 ]; then
	echo 'PASS' >> $TESTRESULT
else
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Successful*" $TESTLOG) -eq 1 ]; then
	echo 'PASS' >> $TESTRESULT
else
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
fi
echo >> $TESTRESULT




TEST="==TEST 5: TESTING FIRST MODE WIHTOUT MODIFIED MODE PATH, SELECTING 1:ALL:3=="
TESTOUT="test5.out"
TESTLOG="test5.log"
rm $TESTLOG $TESTOUT

echo $TEST | tee -a $TESTRESULT
echo -ne '1\n\n3\n1' | python3 ../treesub.py -c input.yaml -l $TESTLOG >> $TESTOUT

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" $TESTOUT) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some files could not be located:" >> $TESTRESULT
if [ $(grep -c "Unable to locate\|" $TESTOUT) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Not found\|Unsuccessful*" $TESTLOG) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo >> $TESTRESULT




TEST="==TEST 6: TESTING SECOND MODE WITH MODIFIED MODE PATH (test-1), SELECTING 1:ALL:3=="
TESTOUT="test6.out"
TESTLOG="test6.log"
rm $TESTLOG $TESTOUT

echo $TEST | tee -a $TESTRESULT
echo -ne '1\n\n3\n2' | python3 ../treesub.py -m 1 -c input.yaml -l $TESTLOG >> $TESTOUT

echo "Checking if all files could be located:" >> $TESTRESULT
if [ $(grep -c "Could not locate\|" $TESTOUT) -eq 1 ]; then
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo "Checking if some files could not be located:" >> $TESTRESULT
if [ $(grep -c "Unable to locate\|" $TESTOUT) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi

echo "Checking if some runs were unsuccessful:" >> $TESTRESULT
if [ $(grep -c "Not found\|Unsuccessful*" $TESTLOG) -eq 1 ]; then
	echo "FAIL" >> $TESTRESULT
	RESULT="FAIL"
else
	echo 'PASS' >> $TESTRESULT
fi
echo >> $TESTRESULT



echo "OVERALL RESULT: $RESULT" | tee -a $TESTRESULT