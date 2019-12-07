import sys
import os
source_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),
                           "3Dpredictor/source")
print (source_path)
sys.path.append(source_path)
from ChiPSeqReader import ChiPSeqReader

print("Hello world")
print("Hello world2")