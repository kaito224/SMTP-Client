
# SMTP Client

A small SMTP-client written in python.


## Requirements
- Python Version 3.6.8 or higher


## How to use
```bash
usage: client.py [-h] [--port PORT] [--fqdn FQDN] [-no-ssl] [-u USERNAME]
                 [-pw PASSWORD] [--sender SENDER]
                 [--recipients RECIPIENTS [RECIPIENTS ...]]
                 [--subject SUBJECT [SUBJECT ...]] [--text TEXT [TEXT ...]]
                 {send,ehlo,healthcheck} server_adress

positional arguments:
  {send,ehlo,healthcheck}
                        Send: Send a mail/nEHlo:ends an EHLO to the smtp
                        server and prints all extensions
  server_adress         The Adress of the smtp server. Either IPv4 Adress or
                        its domain name

options:
  -h, --help            show this help message and exit
  --port PORT           Defines the port to use. If not specified port 587 is
                        used
  --fqdn FQDN           Defines the fully qualified domain name (FQDN) to give
                        to the smt server
  -no-ssl               Do not use ssl/tls when connecting to a mailserver
  -u USERNAME, --username USERNAME
                        Defines the user name to use if the smtp server
                        supports
  -pw PASSWORD, --password PASSWORD
                        Defines the password to use if the smtp server
                        supports. This option is unsafe as the password is
                        given in blank. We highly advise againts this option.
                        The script will ask for the password interactively if
                        this option is omitted
  --sender SENDER       The email adress of the sender
  --recipients RECIPIENTS [RECIPIENTS ...]
                        The email adresses of the recipients
  --subject SUBJECT [SUBJECT ...]
                        The subject of the mail
  --text TEXT [TEXT ...]
                        The text to send
```