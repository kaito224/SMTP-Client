
# SMTP Client

A small SMTP-client written in python.


## Requirements
- Python Version 3.6.8 or higher


## How to
```bash
usage: client.py [-h] [-no-ssl] [-no-mime] [-v] [--port PORT] [--fqdn FQDN]
                 [-u USERNAME] [-pw PASSWORD] [--sender SENDER]
                 [--recipients RECIPIENTS [RECIPIENTS ...]]
                 [--subject SUBJECT [SUBJECT ...]] [--text TEXT [TEXT ...]]
                 [--authentication-method {LOGIN,PLAIN}]
                 [--attachments ATTACHMENTS [ATTACHMENTS ...]]
                 {send,ehlo,healthcheck} server_adress

positional arguments:
  {send,ehlo,healthcheck}
                        send: Send a mail
                        ehlo: sends an EHLO to the smtp server and prints all extensions. Extensions may differ when using ssl
                        healthcheck: Prints the initial message the smtp server sends on connecting via tcp 
  server_adress         The Adress of the smtp server. Either IPv4 Adress or its domain name

options:
  -h, --help            show this help message and exit
  -no-ssl               Do not use ssl/tls when connecting to a mailserver
  -no-mime              Do not use MIME when sending a mail. Subject and attachments will be disregarded
  -v                    Make output more verbose
  --port PORT           Defines the port to use. If not specified port 587 is used
  --fqdn FQDN           Defines the fully qualified domain name (FQDN) to give  to the smt server
  -u USERNAME, --username USERNAME
                        Defines the user name to use if the smtp server supports
  -pw PASSWORD, --password PASSWORD
                        Defines the password to use if the smtp server supports.
                        This option is unsafe as the password is shown in plain.
                        The script will ask for the password interactively if this option is omitted 
  --sender SENDER       The email adress of the sender
  --recipients RECIPIENTS [RECIPIENTS ...]
                        The email adresses of the recipients
  --subject SUBJECT [SUBJECT ...]
                        The subject of the mail
  --text TEXT [TEXT ...]
                        The text to send
  --authentication-method {LOGIN,PLAIN}
                        Chose a SASL method for authentication. Login is set as default
  --attachments ATTACHMENTS [ATTACHMENTS ...]
                        Paths to file attachments
```