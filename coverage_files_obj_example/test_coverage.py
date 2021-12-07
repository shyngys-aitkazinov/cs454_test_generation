import coverage
import signal
def handler(signum, frame):
	print('Timeout of the test case')
	raise Exception('end of time')
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)
cov = coverage.Coverage() 
cov.set_option('run:branch', True) 
cov.start()
try:
	from obj_example import *
except:
	with open("crashed.txt", "w+") as cr_file:
		cr_file.write("yes")
cov.stop()
cov.save()
cov.json_report()
