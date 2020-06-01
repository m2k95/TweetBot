from app import du3aaAPI
import sys

def usage():
    print ("Usage: app.py post|postAll|clean")
    sys.exit

if (len(sys.argv) < 2 ):
    usage()
else:
    if (str(sys.argv[1]) == 'post'):
        app = du3aaAPI()
        app.Post()
    elif (str(sys.argv[1]) == 'postAll'):
        app = du3aaAPI()
        app.Iterate()
    elif (str(sys.argv[1]) == 'clean'):
        app = du3aaAPI()
        app.Clean()
    else:
        usage()
