from app import app, freezer
import sys

import os
sys.path.append(os.getcwd())

app.testing = True
#TODO: turn debugging off
app.debug = True

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)