from socket import * # type: ignore
from commands import *
import argparse
import getpass



def main():

    #parse arguments
    args = parser.parse_args()
    METHOD = args.method
    MAILSERVER = (args.server_adress, args.port)
    PASSWORD = args.password if args.password is not None else None
    USERNAME = args.username if args.username is not None else None
    SENDER = args.sender
    RECIPIENTS = args.recipients
    FQDN = args.fqdn if args.fqdn is not None else ""
    SUBJECT = " ".join(args.subject) if args.subject is not None else ""
    TXTMESSAGE = " ".join(args.text) if args.text is not None else ""

    #open socket and create a tcp connection
    with socket(AF_INET, SOCK_STREAM) as clientSocket:
        
        #connect to mailserver and wait for innit message
        clientSocket.connect(MAILSERVER)
        server_message_innit = clientSocket.recv(1024).decode()
        if server_message_innit[:3] != '220':
            print(f"""220 reply not received from server: {MAILSERVER}""")
            return
        helo_CMD(clientSocket, FQDN)

        #start ssl
        if not args.no_ssl:
            (sslClientSocket, server_message) = starttls_CDM(clientSocket, MAILSERVER[0])
            if sslClientSocket is None:
                print(f"""Could not establish tls connection got error: {server_message}""")
                return
            print("SSL connection has been successfully established")
            helo_CMD(sslClientSocket, FQDN)# I dont know why but you have to send a helo after establishing a ssl/tls connection
            clientSocket = sslClientSocket
        
        #method logic
        if METHOD == "healthcheck":
            print(server_message_innit)
            clientSocket.close()
            return

        if METHOD == "ehlo":
            print(ehlo_CMD(clientSocket, FQDN))
            clientSocket.close()
            return
        
        if METHOD == "send":
            if None in (SENDER, RECIPIENTS):
                print("In order to send the sender and recipients must be defined")
                return
            
            #login
            #TODO : Write function which handles different SAS login methods
            #TODO : Return when login was not successfull
            if PASSWORD is None:
                PASSWORD = getpass.getpass("Password: ")
            server_message_login = authLogin_CMD(sslClientSocket, username=USERNAME, password=PASSWORD)
            print(server_message_login)
            #mail
            #TODO : Check responses
            mail_CMD(clientSocket, SENDER)
            for recipient in RECIPIENTS:
                rcpt_CMD(clientSocket, recipient)
            #data
            #TODO : message constructor which adds each recipient and allows for attachments
            message = message=f"""From: {SENDER}\r\nTo: {RECIPIENTS[0]}\r\nSubject: {SUBJECT}\r\n\r\n{TXTMESSAGE}"""
            server_message_data = data_CMD(clientSocket,message)
            print(server_message_data)
            quit_CMD(clientSocket)

            clientSocket.close()
            return        
    


if __name__ == "__main__":

    #Create ArgumentParser
    parser = argparse.ArgumentParser()

    parser.add_argument("method",
                        choices=["send", "ehlo", "healthcheck"],
                        help="Send: Send a mail/nEHlo:ends an EHLO to the smtp server and prints all extensions")
    
    parser.add_argument("server_adress", 
                        help="The Adress of the smtp server. Either IPv4 Adress or its domain name")
    
    parser.add_argument("--port",
                        type=int,
                        default=587,
                        help=f"""Defines the port to use. If not specified port 587 is used""")

    parser.add_argument("--fqdn",
                        help="Defines the fully qualified domain name (FQDN) to give  to the smt server")

    parser.add_argument("-no-ssl",
                        help="Do not use ssl/tls when connecting to a mailserver", 
                        action="store_true")

    parser.add_argument("-u", 
                        "--username", 
                        help="Defines the user name to use if the smtp server supports")

    parser.add_argument("-pw", 
                        "--password", 
                        help=f"""Defines the password to use if the smtp server supports. This option is unsafe as the password is given in blank.
                        We highly advise againts this option. The script will ask for the password interactively if this option is omitted """)

    parser.add_argument("--sender",
                        help="The email adress of the sender")

    parser.add_argument("--recipients",
                        nargs="+",
                        help="The email adresses of the recipients")
    
    parser.add_argument("--subject",
                        nargs="+",
                        help="The subject of the mail")
    
    parser.add_argument("--text",
                        nargs="+",
                        help="The text to send")


    #call main
    main()