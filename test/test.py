#!/usr/bin/python3

import os
import yaml
from treerun.main import convert_placeholders, tabulate
import subprocess


# template command:
# echo -ne '\n\n\n1' | python3 ../src/treerun/main.py -i input.yaml -o "logs/$TESTLOG" >> "logs/$TESTOUT"
if __name__ == '__main__':
	EXIT_CODE = None
	RETURN_CODE = 0

	file = 'tests.yaml'
	base_python_cmd = 'python3 ../src/treerun/main.py'


	if os.path.isfile(file):
		with open(file, 'r') as f:
			conf = yaml.safe_load(f)
		f.close()

	cwd = os.getcwd()
	
	input_file = conf['input']
	log_dir = conf['logdir']
	for file in os.listdir(log_dir):

		os.remove(f'{log_dir}{file}')

	results = {}
	for i, (test, definition) in enumerate(conf['tests'].items()):
		results[test] = {}
		placeholders = {
			'name':test,
		}
		definition = convert_placeholders(definition,placeholders)

		prompt_selection = r'\n'.join([l for l in str(definition['selection'])])#+r'\n'
		log = log_dir+definition['log']
		stdout = log_dir+definition['stdout']

		if 'all' in definition.keys():
			# run with -a
			if 'mod' in definition.keys():
				modifier = definition['mod']
				cmd = f'echo \'{prompt_selection}\' | {base_python_cmd} -i {input_file} -o {stdout} -m {modifier} -a >> {log}'
			else:
				cmd = f'echo \'{prompt_selection}\' | {base_python_cmd} -i {input_file} -o {stdout} -a >> {log}'
		else:
			# do NOT run with -a
			if 'mod' in definition.keys():
				modifier = definition['mod']
				cmd = f'echo \'{prompt_selection}\' | {base_python_cmd} -i {input_file} -o {stdout} -m {modifier} >> {log}'
			else:
				cmd = f'echo \'{prompt_selection}\' | {base_python_cmd} -i {input_file} -o {stdout} >> {log}'

		return_code = subprocess.call(cmd, shell=True)

		# Splits a given string at every digit, and converts all elements to 
		# integers, causing strings to be effectively dropped.
		extract_digit = lambda x: [int(s) for s in x.split() if s.isdigit()][0]
		with open(f'{cwd}/{log}', 'r') as f:
			for line in f.readlines():
				if 'exit code' in line:
					exit_code = extract_digit(line)
				else:
					exit_code = None
		results[test]['exit code'] = exit_code
		results[test]['return code'] = return_code



		if (return_code == 0) and (exit_code is None):
			os.remove(f'{cwd}/{log}')
		
		if exit_code is None:
			os.remove(f'{cwd}/{stdout}')


	RETURN_CODE = return_code; EXIT_CODE = EXIT_CODE
	if (RETURN_CODE != 0) and (EXIT_CODE != None):	
		for key,val in results.items():
			print(key)
			for k,v in val.items():
				print(f'\t{k}:\t\t{v}')
	else:
		print('All tests passed!')