import traceback
import sys
try:
    import app.main
    print('OK')
except Exception as e:
    traceback.print_exc(file=sys.stdout)
