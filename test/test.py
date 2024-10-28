#!/usr/bin/python3

import os
import yaml
from treerun.main import convert_placeholders, whitespace
import subprocess
import pandas as pd

# template command:
# echo -ne '\n\n\n1' | python3 ../src/treerun/main.py -i input.yaml -o "logs/$TESTLOG" >> "logs/$TESTOUT"
if __name__ == '__main__':
	file = 'tests.yaml'
	base_python_cmd = 'python3 ../src/treerun/main.py'

	# Load test config
	if os.path.isfile(file):
		with open(file, 'r') as f:
			conf = yaml.safe_load(f)
		f.close()

	# Path variables
	cwd = os.getcwd()
	input_file = conf['input']
	log_dir = conf['logdir']

	# Clear old data
	if not os.path.isdir(log_dir):
		os.mkdir(log_dir)
	for file in os.listdir(log_dir):
		os.remove(f'{log_dir}{file}')

	results = {}
	for i, (test, definition) in enumerate(conf['tests'].items()):
		# Map placeholders
		placeholders = {
			'name':test,
		}
		definition = convert_placeholders(definition,placeholders)


		# Output paths
		log = log_dir+definition['log']
		stdout = log_dir+definition['stdout']

		# Generate run command
		prompt_selection = r'\n'.join([l for l in str(definition['selection'])])#+r'\n'
		if 'all' in definition.keys():
			# run with -a
			if 'mod' in definition.keys():
				modifier = definition['mod']
				cmd = f'echo \'{prompt_selection}\' | {base_python_cmd} -i {input_file} -o {log} -m {modifier} -a >> {stdout}'
			else:
				cmd = f'echo \'{prompt_selection}\' | {base_python_cmd} -i {input_file} -o {log} -a >> {stdout}'
		else:
			# do NOT run with -a
			if 'mod' in definition.keys():
				modifier = definition['mod']
				cmd = f'echo \'{prompt_selection}\' | {base_python_cmd} -i {input_file} -o {log} -m {modifier} >> {stdout}'
			else:
				cmd = f'echo \'{prompt_selection}\' | {base_python_cmd} -i {input_file} -o {log} >> {stdout}'

		# Program call
		return_code = subprocess.call(cmd, shell=True)

		# Splits a given string at every digit, and converts all elements to 
		# integers, causing strings to be effectively dropped.
		extract_digit = lambda x: [int(s) for s in x.split() if s.isdigit()][0]
		exit_code = None
		with open(f'{cwd}/{stdout}', 'r') as f:
			for line in f.readlines():
				if 'exit code:' in line:
					exit_code = extract_digit(line)

		# Gather expected results
		expected_return = definition['expectation']['return code']
		expected_exit = definition['expectation']['exit code']
		
		#print(test, exit_code, expected_exit)

		# Check if results match
		if (exit_code == expected_exit) and (return_code == expected_return):
			try:
				os.remove(f'{cwd}/{log}')
			except:
				exit_code = 1
			try:
				os.remove(f'{cwd}/{stdout}')
			except:
				pass

		else:
			results[test] = {}
			results[test]['expectation'] = definition['expectation']
			results[test]['outcome'] = {
				'return code':return_code,
				'exit code':exit_code,
			}

		#if (return_code == 0) and (exit_code is None):
		#if exit_code is None:

	#print(results)
	#treeview(results)
	#w = whitespace(results, tab_width=4, max_length=None)
	#print(w)
	#tabulate(results)
	#df = pd.DataFrame.from_dict(results, orient='index')
	df = pd.DataFrame(results)
	print('Result:')
	if results == {}:
		print('All tests passed!')
	else:
		print('The following tests failed:')
		print(df)

	print('\nExplanations:')
	print('Return code 0 means that the program was executed without problems')
	print('Exit code 0 means that the necessary files could not be found')
	print('Exit code 1 means that there was a problem with some selection')
