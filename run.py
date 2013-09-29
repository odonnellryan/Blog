import sys
import os

from app import app


sys.path.append(os.getcwd())

app.testing = True
#TODO: turn debugging off
app.debug = True

if __name__ == '__main__':
    app.run(port=8000)