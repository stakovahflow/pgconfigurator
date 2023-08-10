#!/usr/bin/env python3
# Last modified: 2023-05-23
from datetime import datetime
import sys
import argparse
import os

debugging=False
RAM=0
CPU=0
DISK=False
size = os.get_terminal_size().columns
def LINE():
	print('-'*size)

def morehelp():
	LINE()
	print('Example Usage: ')
	print('%s -cpu 16 -mem 32 -disk ssd' % (sys.argv[0]))
	print('%s -c 32 -m 64 -d hdd\n' % (sys.argv[0]))

#######################################################################
# Add some command line arguments for easier use:
parser = argparse.ArgumentParser(description='Provide Customizations for Forescout eyeInspect PostgreSQL configuration')
parser.add_argument('-m', '--mem', type=str, help='Memory installed in Command Center')
parser.add_argument('-c', '--cpu', type=str, help='CPU threads (typically double Virtual CPU count)')
parser.add_argument('-d', '--disk', type=str, help='SSD (default) or HDD')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

# Consolidate our command line arguments:
args=parser.parse_args()

if args.verbose:
	debugging = True
if debugging:
	print('Debugging on')
try:
	if args.cpu:
		CPU=int(args.cpu)
	else:
		CPU=int(input('System ' + '\033[1m' + 'CPU'+ '\033[m' + ' Threads (integer): '))

	if args.mem:
		RAM=int(args.mem)*1024
	else:
		RAM=int(input('System ' + '\033[1m' + 'Memory'+ '\033[m' + ' (in GB) (integer): '))*1024
	if RAM < 1:
		exit(1)

	if args.disk:
		DISK=args.disk.lower()
	else:
		DISK=input('System ' + '\033[1m' + 'Disk'+ '\033[m' + ' Selection [' + '\033[1m' + 'ssd*'+ '\033[m' + ', hdd]: ')
	if DISK == 'hdd':
		random_page_cost='2.0'
		DISKTYPE='Mechanical'
	elif DISK == 'ssd':
		random_page_cost='1.0'
		DISKTYPE='Solid State'
	elif DISK == '':
		random_page_cost='1.0'
		DISKTYPE='Solid State'
	else:
		exit(1)

	if debugging:
		LINE()
		print('System CPU thread count: %d' % (CPU))
		print('System Memory: %d GB' % (RAM))
		print('System Disk: %s' % (DISKTYPE))
except:
	
	#print('\033[1m')
	LINE()
	print('Invalid arguments/options provided')
	parser.print_help()
	morehelp()
	LINE()
	#print('\033[0m' + '')
	exit(0)

#######################################################################
# Meat and potatoes:
print('Please make a backup of the current postgresql.conf, copy the following text, and update the existing with the following:')
LINE()

# From sd_pgtune:
shared_buffers=(RAM / 4)
work_mem=(RAM / 200)
maintenance_work_mem=(RAM / 100)
effective_cache_size=(RAM / 2)
effective_io_concurrency=200
max_worker_processes=(CPU / 2)
max_parallel_maintenance_workers=(CPU / 4)
max_parallel_workers_per_gather=(CPU / 8)
max_parallel_workers=(CPU / 2)
default_statistics_target=200

print('# Forescout eyeInspect Custom Settings:')
print('max_connections = 256') # Static setting
print('shared_buffers = %dMB' % (shared_buffers))
print('work_mem = %dMB' % (work_mem))
print('maintenance_work_mem = %dMB' % (maintenance_work_mem))
print('effective_cache_size = %dMB' % (effective_cache_size))
print('effective_io_concurrency = %d' % (effective_io_concurrency))
print('max_worker_processes = %d' % (max_worker_processes))
print('max_parallel_maintenance_workers = %d' % (max_parallel_maintenance_workers))
if max_parallel_workers_per_gather >= 1:
	print('max_parallel_workers_per_gather = %d' % (max_parallel_workers_per_gather))
	# If less than 1, this setting should not be used
print('max_parallel_workers = %d' % (max_parallel_workers))
print('max_wal_size = 4GB') # Static setting
print('min_wal_size = 1GB') # Static setting
print('checkpoint_completion_target = 0.9') # Static setting
print('random_page_cost = %s' % (random_page_cost))
print('default_statistics_target = %s' % (default_statistics_target))
print('jit = on\n') # Static setting

LINE()
