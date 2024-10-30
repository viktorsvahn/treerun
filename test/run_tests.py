#!/usr/bin/python3

import os
import yaml
from treerun.main import convert_placeholders, whitespace, ExitCode
import subprocess
from tabulate import tabulate


# template command:
# echo -ne '\n\n\n1' | python3 ../src/treerun/main.py -i input.yaml -o "logs/$TESTLOG" >> "logs/$TESTOUT"
if __name__ == '__main__':
	file = 'test_setup.yaml'
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

	results = []
	for i, (test, definition) in enumerate(conf['tests'].items()):
		print(f"Testing: {test}\nDescription: {definition['desc']}")
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

		# Check if results match
		if (exit_code == expected_exit) and (return_code == expected_return):
			print('PASS\n')
			try:
				os.remove(f'{cwd}/{log}')
			except:
				pass
				#print(f'Could not remove {log}')
			try:
				os.remove(f'{cwd}/{stdout}')
			except:
				pass
				#print(f'Could not remove {stdout}')

		else:
			print('FAIL\n')
			outcome = [
				test,
				expected_return,
				return_code,
				expected_exit,
				exit_code
			]
		
			try:
				results.append(outcome)
			except:
				pass


	# Creating a table with headers and a grid format
	table = tabulate(
	    results, 
	    headers=["Test", "Expected return code", "Return code", "Expected code", "Exit code"], 
	    #tablefmt="grid"
	)
	if len(results) > 0:
		print(table)

		codes = ExitCode().legend
		print('\nCode:\tInterpretation:')
		for key,val in codes.items():
			print(f'\t{key}\t{val}')
	else:
		print('All tests passed!')
