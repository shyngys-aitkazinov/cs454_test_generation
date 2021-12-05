import coverage
cov = coverage.Coverage() 
cov.start()
from queue_example import *
v0 = 853
v1 = Queue(v0 )
v2 = Queue(v0 )
v3 = v1.enqueue( v0 )
v4 = v1.empty(  )
v5 = v1.full(  )
v6 = v1.dequeue(  )
v7 = dummyadd( v0, v0 )
v8 = dummyadd( v0, v0 )
cov.stop()
cov.save()
cov.json_report()
