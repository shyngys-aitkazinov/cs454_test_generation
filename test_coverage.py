import coverage
cov = coverage.Coverage() 
cov.start()
from queue_example import *
v0 = 401
v1 = dummyadd( v0, v0 )
v2 = Queue(v0 )
v3 = dummyadd( v0, v0 )
v4 = dummyadd( v0, v0 )
v5 = dummyadd( v0, v0 )
v6 = v2.empty(  )
v7 = v2.empty(  )
v8 = dummyadd( v0, v0 )
cov.stop()
cov.save()
cov.json_report()
