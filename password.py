import sys
import getopt
import login


def reset(argv) :
    try :
        options, arguments = getopt.getopt(argv, "hu:p:e:")
    except getopt.GetoptError, e :
        print 'Opt Error: password.py -u <username> -p <password> -e <email>' + str(e)
        sys.exit(2)
    updated = []
    for opt, arg in options :
        if opt == '-h' :
            print 'Help: password.py -u <username> -p <password> -e <email>'
            sys.exit()
        if opt == '-p' :
            login.update_password_no_username(arg)
            updated.append('password')
        if opt == '-u' :
            login.update_username(arg)
            updated.append('username')
        if opt == '-e' :
            login.update_email(arg)
            updated.append('email')
    if updated :
        print "Updated: " + ", ".join(updated)
    else :
        print "No values updated"


if __name__ == "__main__" :
    reset(sys.argv[1 :])
