import example

import coverage

cov = coverage.Coverage()
cov.start()

x = 495
y = -480
z = -460
v0 = example.triangle( x, y, z )

cov.stop()
cov.save()

cov.json_report()