
# SMTP Client

A small SMTP-client written in python.


## Requirements
- Python Version 3.6.8 or higher


## How to
Make sure that client.py and commands.py are in the working directory before calling client.py

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
                        healthcheck: Prints the initial message from the server. Does not establish ssl connection
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

## Examples
### Send a message
In the following example we use the *mail.uni-mainz.de* server to send an email from *me@students.uni-mainz.de* to *neuwirth@uni-mainz.de* and *bartelheimer@uni-mainz.de*. We use the username *me* to authenticate<br />
The content of the message is the string *hello world*. The subject is *Hello World Test* and we attach two files.

```bash
python3 client.py send mail.uni-mainz.de --sender=me@students.uni-mainz.de --recipients neuwirth@uni-mainz.de bartelheimer@uni-mainz.de --username=me  --text hello world --subject Hello World Test --attachments /path_to_file1 /path_to_file2
```

### EHLO
We use the ehlo mode to get all extensions of the server smtp.gmail.com
```bash
python3 client.py ehlo smtp.gmail.com
```

We get the following output:
```
250-smtp.gmail.com at your service, [134.93.214.186]
250-SIZE 35882577
250-8BITMIME
250-AUTH LOGIN PLAIN XOAUTH2 PLAIN-CLIENTTOKEN OAUTHBEARER XOAUTH
250-ENHANCEDSTATUSCODES
250-PIPELINING
250-CHUNKING
250 SMTPUTF8
```

ESMTP allows for a server to give a different output for the EHLO command based on whether ssl/tls is enabled or not. We can disable SSL with the `-no-ssl` flag an get the following output.

```bash
python3 client.py ehlo smtp.gmail.com -no-ssl
250-smtp.gmail.com at your service, [134.93.214.186]
250-SIZE 35882577
250-8BITMIME
250-STARTTLS
250-ENHANCEDSTATUSCODES
250-PIPELINING
250-CHUNKING
250 SMTPUTF8
```

### Healthchek
We perform a healtcheck for *smtp.web.de*.<br />
In *healthcheck* mode we establish a tcp connection with the server and print its initial response. Then we close the tcp connection without issuing any commands. Therefore healthchecks are not affected by the `-no-ssl` flag as we don't establish a ssl/tls session from the get go. 
```bash
python3 client.py healthcheck smtp.web.de
```

```
220 web.de (mrweb105) Nemesis ESMTP Service ready
```