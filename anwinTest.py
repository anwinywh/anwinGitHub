
import os
import os.path
import sys

workDir = os.path.split( os.path.realpath( sys.argv[0] ) )[0]

print "workDir:" + workDir

workDir = os.path.dirname(workDir)
print "workDir:" + workDir