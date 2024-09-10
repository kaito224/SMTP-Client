from socket import * # type: ignore
from commands import *
import argparse
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List


def authenticate(socket: socket, username:str, password, authentication_method = "LOGIN"):
    #TODO : Handle more SAS login methods

    if authentication_method == "LOGIN":
        return authLogin_CMD(socket, username, password)

    if authentication_method == "PLAIN":
        return authPlain_CMD(socket, username, password)
    
    raise Exception("authentication method did not match implemented methods")


def create_mime(sender: str, recipients, subject: str, textpayload: str, attachment_paths: List[str]) -> str:
    #Header
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    #Payload
    message.attach(MIMEText(textpayload))
    if not attachment_paths:                 #Just return if there are no attachments
        return message.as_string()
    
    #attach files
    for path in attachment_paths:
        with open(path, "rb") as f:
            data = f.read()
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(data)
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", f'attachment; filename="{path.split("/")[-1]}"')
            message.attach(payload=attachment)
    return message.as_string()


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
    AUTHENTICATION_METHOD = args.authentication_method
    ATTACHMENT_PATHS = args.attachments if args.attachments is not None else []
    VERBOSE = args.v

    #open socket and create a tcp connection
    with socket(AF_INET, SOCK_STREAM) as clientSocket:
        
        #connect to mailserver and wait for innit message
        clientSocket.connect(MAILSERVER)
        if VERBOSE: print(f"""Opened tcp socket and sucessfully connected to mailserver: {MAILSERVER}""")
        server_message_innit = clientSocket.recv(1024).decode()
        if server_message_innit[:3] != '220':
            print(f"""220 reply not received from server: {MAILSERVER}""")
            return
        helo_CMD(clientSocket, FQDN) #send initial hello

        #start ssl
        if not args.no_ssl:
            (sslClientSocket, server_message_ssl) = starttls_CDM(clientSocket, MAILSERVER[0])
            if sslClientSocket is None:
                print(f"""Could not establish tls connection got error: {server_message_ssl}""")
                return
            if VERBOSE: print(f"SSL connection has been successfully established")
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
            
            #authentication
            if USERNAME is None:
                print("A username must be defined to authenticate to a server")
                return
            if PASSWORD is None:
                PASSWORD = getpass.getpass("Password: ")

            if VERBOSE: print("Starting Authentification......")
            server_message_authentication = authenticate(clientSocket, USERNAME, PASSWORD, AUTHENTICATION_METHOD)
            if server_message_authentication[:3] != "235" : 
                print(f"""Could not authenticate. Got server error: {server_message_authentication}""")
                return
            if VERBOSE: print(f"""Authentification was successfull. Got server message: {server_message_authentication}""")
            
            #mail
            server_message_mail = mail_CMD(clientSocket, SENDER)
            if server_message_mail[:3] != "250":
                print(f"""Mail command failed. Got server error: {server_message_mail}""")
                return
            if VERBOSE: print(f"""Sucessfully send Mail command (from {SENDER}). Got server message: {server_message_mail}""")
            
            for recipient in RECIPIENTS:
                server_message_rcpt = rcpt_CMD(clientSocket, recipient)
                if server_message_rcpt[:3] != "250":
                    print(f"""RCPT command failed for {recipient}. Got server error: {server_message_rcpt}""")
                    return
                if VERBOSE: print(f"""Sucessfully send RCPT command for recipient: {recipient}. Got server message: {server_message_mail}""")

            #data
            if args.no_mime:
                message = TXTMESSAGE
            else:   
                message = create_mime(SENDER,RECIPIENTS,SUBJECT,TXTMESSAGE,ATTACHMENT_PATHS)
            server_message_data = data_CMD(clientSocket,message)
            if server_message_data[:3] != "250":
                    print(f"""DATA command failed. Got server error: {server_message_data}""")
                    return
            print(f"""Email was send. Received Server message: {server_message_data}""")

            #quit
            quit_CMD(clientSocket)

            clientSocket.close()
            return        
    


if __name__ == "__main__":

    #Create ArgumentParser
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("method",
                        choices=["send", "ehlo", "healthcheck"],
                        help="send: Send a mail\nehlo: sends an EHLO to the smtp server and prints all extensions. Extensions may differ when using ssl\nhealthcheck: Prints the initial message the smtp server sends on connecting via tcp ")
    
    parser.add_argument("server_adress", 
                        help="The Adress of the smtp server. Either IPv4 Adress or its domain name")
    
    parser.add_argument("-no-ssl",
                        help="Do not use ssl/tls when connecting to a mailserver", 
                        action="store_true")
    
    parser.add_argument("-no-mime",
                        help="Do not use MIME when sending a mail. Subject and attachments will be disregarded", 
                        action="store_true")
    
    parser.add_argument("-v",
                        help="Make output more verbose", 
                        action="store_true")
    
    parser.add_argument("--port",
                        type=int,
                        default=587,
                        help=f"""Defines the port to use. If not specified port 587 is used""")

    parser.add_argument("--fqdn",
                        help="Defines the fully qualified domain name (FQDN) to give  to the smt server")

    parser.add_argument("-u", 
                        "--username", 
                        help="Defines the user name to use if the smtp server supports")

    parser.add_argument("-pw", 
                        "--password", 
                        help=f"""Defines the password to use if the smtp server supports.\nThis option is unsafe as the password is shown in plain.\nThe script will ask for the password interactively if this option is omitted """)

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
    
    parser.add_argument("--authentication-method",
                        choices=["LOGIN", "PLAIN"],
                        default = "LOGIN",
                        help="Chose a SASL method for authentication. Login is set as default")
    
    parser.add_argument("--attachments",
                        nargs="+",
                        help="Paths to file attachments")


    #call main
    main()