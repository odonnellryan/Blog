from app import app, freezer
import sys
app.testing = True
#TODO: Turn Debug off...

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)