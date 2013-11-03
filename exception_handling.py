import peewee
import sqlite3
import _mysql_exceptions
import messages

database_exceptions = (_mysql_exceptions.OperationalError, peewee.ImproperlyConfigured, _mysql_exceptions.ProgrammingError,
                      sqlite3.OperationalError, sqlite3.ProgrammingError, peewee.DoesNotExist)

def database_exception_handler(exception):
    redirect = None
    error = messages.ERROR_DATABASE_CONFIGURATION
    #if the tables aren't properly configured (ProgrammingError exception raised code 1146)
    if 1146 in exception.args:
        redirect = 'config.db_tables'
        error = 'improper_tables'
    #check if it's an auth error (in this case most likely db info isn't set correctly)
    if 1045 in exception.args:
        error = messages.ERROR_DATABASE_CONFIGURATION
    #this is because the database isn't configured correctly, eg tables etc..
    if 1054 in exception.args:
        pass
        #db_mods.create_tables()
    #check if there is any database configuration stuff. if there is not, redirect to the install page
    return error, redirect