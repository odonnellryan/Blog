import sys
import getopt
import login


def reset(argv):
    try:
        options, arguments = getopt.getopt(argv, "hu:p:e:")
    except getopt.GetoptError, e:
        print 'Opt Error: password.py -u <username> -p <password>' + str(e)
        sys.exit(2)
    updated = []
    for opt, arg in options:
        if opt == '-h':
            print 'Help: password.py -u <username> -p <password>'
            sys.exit()
        if opt == '-p':
            login.change_login_details(None, arg)
            updated.append('password')
        if opt == '-u':
            login.change_login_details(arg, None)
            updated.append('username')
    if updated:
        print "Updated: " + ", ".join(updated)
    else:
        print 'Help: password.py -u <username> -p <password>'


if __name__ == "__main__":
    reset(sys.argv[1:])
