import coverage
cov = coverage.Coverage() 
cov.set_option('run:branch', True) 
cov.start()
from queue_example import *
v0 = 455
v1 = Queue(v0 )
v2 = dummyadd( v0, v0 )
cov.stop()
cov.save()
cov.json_report()
