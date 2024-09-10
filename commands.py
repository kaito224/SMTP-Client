from socket import * # type: ignore
import ssl
import base64

#TODO: Encoding ascii/utf-8
#TODO: Add verbosity option

# HELO command to initiate a converstaion with a smtp server and provide the server with own fqdn
def helo_CMD(socket: socket, fqdn: str) -> str:
    """Send HELO command and returns server response."""

    heloCommand = 'HELO fqdn\r\n'
    socket.send(heloCommand.encode())
    server_response = socket.recv(1024).decode()
    return server_response


# ELHO command
def ehlo_CMD(socket: socket, fqdn: str) -> str:
    """Send EHLO command and returns server response."""

    heloCommand = 'EHLO fqdn\r\n'
    socket.send(heloCommand.encode())
    server_response = socket.recv(1024).decode()
    return server_response


# MAIL command. This command states the reverse_path for a mail i.e. the sender address
def mail_CMD(socket: socket, reverse_path: str) -> str:
    """Send MAIL FROM command and return server response."""

    mailCommand = f"""MAIL FROM:<{reverse_path}>\r\n"""
    socket.send(mailCommand.encode())
    server_response = socket.recv(1024).decode()
    return server_response


# RCPT command. This command states the forward-path for a mail i.e. the recipient address
def rcpt_CMD(socket: socket, forward_path: str) -> str:
    """Send RCPT TO command and return the server response. """

    rcptCommand = f"""RCPT TO:<{forward_path}>\r\n"""
    socket.send(rcptCommand.encode())
    server_response = socket.recv(1024).decode()
    return server_response


# Data command. This command sends data to the smtp server
def data_CMD(socket: socket, message: str) -> str:
    """Send DATA command and return server response."""

    #send data command to see if server excepts data
    socket.send("DATA\r\n".encode())
    server_response_datacommand = socket.recv(1024).decode()
    if server_response_datacommand[:3] != '354':
        raise Exception(f"DATA command failed. The smtp server returned: {server_response_datacommand}")
    
    # Send message data
    # TODO: implement dot-stuffing and check if sending data was successfull
    endmsg = "\r\n.\r\n"
    socket.sendall( message.encode() + endmsg.encode() )
    server_response_datatransfer = socket.recv(1024).decode()
    if server_response_datatransfer[:3] != '250':
        raise Exception(f"Data transfer failed. The smtp server returned: {server_response_datatransfer}")
    return server_response_datatransfer


# QUIT command. This command quits a smtp session
def quit_CMD(socket: socket) -> str:
    """Send Quit FROM command and return server response."""

    socket.send("QUIT\r\n".encode())
    server_response = socket.recv(1024).decode()
    return server_response


# STARTTLS command. This command starts a tls/ssl session for smtp. Initiates the handshake
def starttls_CDM(socket: socket, server_hostname: str): #-> tuple[ssl.SSLSocket, str]:
    """Starts TLS command and either returns (none,server message) or a the ssl-interface for the socket and the server message"""

    # Ask for TLS/SSL capabilty by issuing starttls command
    socket.send("STARTTLS\r\n".encode())
    server_response = socket.recv(1024).decode()
    if server_response[:3] != '220':
        return (None, server_response)
        
    #create ssl socket
    # TODO: put in try catch block
    context = ssl.create_default_context()
    ssl_socket =  context.wrap_socket(socket,server_hostname=server_hostname)
    return (ssl_socket, server_response)


# AUTH command which uses the SASL-PLAIN mechanism.
def authPlain_CMD(socket: socket, username, password) -> str:
    """Send auth command using the SASL-PLAIN mechanism and return server response."""

    base64_str = ("\x00" + username + "\x00" + password).encode()
    base64_str = base64.b64encode(base64_str)
    authMsg = "AUTH PLAIN ".encode() + base64_str + " \r\n".encode()
    socket.send(authMsg)
    server_response = socket.recv(1024).decode()
    return server_response


# AUTH command which uses the SASL-LOGIN mechanism.
def authLogin_CMD(socket: socket, username, password) -> str:
    """Send auth command using the SASL-LOGIN mechanism and return server response."""

    #TODO Check each server responses. They are base64 encoded.
    # Some Logins only require a password
    socket.send("AUTH LOGIN \r\n".encode())
    server_response = socket.recv(1024).decode()
    if server_response[:3] != "334": return server_response # return faulty login

    socket.send(base64.b64encode(username.encode()))
    socket.send("\r\n".encode())
    server_response = socket.recv(1024).decode()

    socket.send(base64.b64encode(password.encode()))
    socket.send("\r\n".encode())
    server_response = socket.recv(1024).decode()

    return server_response
