# Import smtplib for the actual sending function
import smtplib
import mimetypes
import sys, traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(you, outFile, logFile):


    COMMASPACE = ', '

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'V-Wrap run result'
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = 'VWrapAdmin@apple.com'
    msg['To'] = you
    msg.preamble = 'V-Wrap run result'

    body = """Hi,

    Attached is the result of the V-Wrap run. More details logged in file %s

""" % (logFile)

    msg.attach(MIMEText(body, 'plain'))

    ctype, encoding = mimetypes.guess_type(outFile)

    maintype, subtype = ctype.split('/', 1)
    print maintype
    print subtype

    fp = open(outFile, 'rb')
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()

    attachment.add_header('Content-Disposition', 'attachment', filename=outFile)
    msg.attach(attachment)

    # Send the email via our own SMTP server.
    s = smtplib.SMTP('relay.apple.com')
    s.sendmail('VWrapAdmin@apple.com',you, msg.as_string())
    s.quit()

if __name__ == "__main__":
    try:
        print len(sys.argv)
        if len(sys.argv) == 4:
            send_mail(sys.argv[1],sys.argv[2],sys.argv[3])
            print sys.argv[1]
            print sys.argv[2]
            print '*******',sys.argv[3]
        else:
            print "Please pass <Receivermailid> <attachmentPath> <LogFilePath>"
            sys.exit(1)
    except Exception:

        print "Error: unable to send email"
        print traceback.format_exc()
