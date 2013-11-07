"""

    Used to define any messages or user communication for the site.
    Enables reuse of error messages, rewriting of messages,etc.

"""

ERROR_POST_DOES_NOT_EXIST = "Sorry, but that post does not seem to exist."
ERROR_DATABASE_CONNECTION = "<p>Sorry, there seems to be a problem with the database connection. This is most often" \
                            " because of a connection error, such as the database server not running or not being" \
                            " configured properly. " \
                            "</p><p>" \
                            "If you have confirmed that your database is running, please navigate to the " \
                            "</p><p>" \
                            "This blog was created using MariaDB (a replacement for MySQL), however, the included" \
                            " PeeWee ORM supports Sqlite, MySQL and Postgresql. It is suggested that one reads" \
                            " up on the differences between these databases before selecting one. However, MariaDB or" \
                            " MySQL have proven to be a safe choice for this type of application."
ERROR_DATABASE_CONFIGURATION = "Sorry, we could not establish a database connection. There may be a problem with" \
                               " the user credentials and database information in your config file."
ERROR_USER_ALREADY_CONFIGURED = "Sorry, but it seems there is already a user configured in your database. Please try to " \
                                " see if you can delete the information and try again."
ERROR_404 = "Sorry, but the page you're looking for can not be found."

# general status messages

MESSAGE_NEW_INSTALL = "Seems as if this is a new install. To continue..."

##### user related messages (account, posting errors, etc..)

# start error messages
ERROR_USER_INFO_INCORRECT = "Sorry, but the information you entered was not correct."
ERROR_ACTION_NOT_CONFIRMED = "Sorry, you did not confirm your action. Either press the confirmation button for this " \
                             "action <a href='/admin/'>or return to the admin homepage.</a>"
ERROR_PASSWORDS_DONT_MATCH = "Your passwords do not match. Please try again."
ERROR_UPDATING_INFO = "There was an error updating your information. Please try again."

def ERROR_CODE_RETURN(error):
    return "Error returned: " + error

# start status messages

def MESSAGE_POST_DELETED(post):
    return 'Post successfully deleted: ' + post

MESSAGE_UPDATED_DATA = "Successfully updated blog data."