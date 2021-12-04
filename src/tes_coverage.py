import coverage
cov = coverage.Coverage() 
cov.start()
import example
x = 4
y = 916
z = 487
v0 = example.triangle( x, y, z )
cov.stop()
cov.save()
cov.json_report()
