import sys
from app import app
import os
sys.path.append(os.getcwd())

app.testing = True
#TODO: turn debugging off
app.debug = True

if __name__ == '__main__':
    app.run(port=8000)