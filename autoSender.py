'''
###########################################################
#                                                         #
#    autoSender : How to Send Automatic Emails            #
#    author     : a.buccato                               #
#    version    : 1.0                                     #
#                                                         #
###########################################################
'''

from time import sleep
import sys, os ,smtplib, json, getpass, mimetypes
from email.message import EmailMessage

toaddrs = json.load(open('assets/address.json'))
server  = json.load(open('assets/config.json'))['server']
port    = json.load(open('assets/config.json'))['port']


def attachFile(message, path, filename):
    with open(path+filename, 'rb') as fp:
        file_data = fp.read()
        maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
        message.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)


def autoSend():
    print('\nStart...')
    fromaddr = input('\nEnter your email address: ')
    password = getpass.getpass()

    with open('assets/mobject.txt', 'r') as fobj, open('assets/mcontent.txt', 'r') as fcnt:
        msg = EmailMessage()
        msg['Subject'] = fobj.read()
        msg['From'] = fromaddr
        msg.set_content(fcnt.read())
        sys.stdout.buffer.write(msg.as_bytes())

    print('\nLoad attachments')
    path  = 'attachments/'
    files = os.listdir(path)
    for file in files:
        attachFile(msg, path, file)

    while True:
        entry = int(input('\nEnter 0 to break, 1 to continue: '))
        if entry == 0:
            print('\n\nAborted')
            break
        elif entry == 1:
            sleep(1)
            try:
                print('\nServer Acknowledge...')
                email = smtplib.SMTP(server, port)
                email.ehlo()
            except socket.error as err:
                playout_logger.error(err)
                email = None
            
            sleep(1)
            if email is not None:
                print(email.starttls())

                try:
                    print('\nLogin...')
                    login = email.login(fromaddr, password)
                except smtplib.SMTPAuthenticationError as serr:
                    playout_logger.error(serr)
                    login = None

                if login is not None:
                    count = len(toaddrs)
                    print('\nSending...')

                    for key, addrs in toaddrs.items():
                        print(f'Email: {count}')
                        email.sendmail(fromaddr, addrs, msg.as_string())
                        count -= 1

                    sleep(1)
                    email.quit()
            print('\n\nDone')
            break
        else:
            print('\nInvalid argument, please, try again')


if __name__ == '__main__':
    print(__doc__)
    autoSend()
