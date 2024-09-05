from socket import * # type: ignore
import ssl



# HELO command to initiate a converstaion with a smtp server and provide the server with own fqdn
def helo_CMD(socket: socket, fqdn: str) -> str:
    """Send HELO command and returns server response."""

    heloCommand = 'HELO fqdn\r\n'
    socket.send(heloCommand.encode())
    server_response = socket.recv(1024).decode()
    return server_response


# ELHO command
def elho_CMD(socket: socket, fqdn: str) -> str:
    return "not implemented yet"


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
    socket.sendall(f"""DATA\r\n""".encode())
    server_response = socket.recv(1024).decode()
    if server_response[:3] != '354':
        raise Exception(f"DATA command failed. The smtp server returned: {server_response}")
    
    # Send message data
    # TODO: implement dot-stuffing
    endmsg = "\r\n.\r\n"
    socket.sendall(( message + endmsg ).encode())

    server_response = socket.recv(1024).decode()
    # if server_response[:3] != '250':
    #     raise Exception(f"text transfer failed. The smtp server returned: {server_response}")
    return server_response


# QUIT command. This command quits a smtp session
def quit_CMD(socket: socket, ) -> str:
    """Send Quit FROM command and return server response."""

    socket.send("QUIT\r\n".encode())
    server_response = socket.recv(1024).decode()
    return server_response


# STARTTLS command. This command starts a tls/ssl session for smtp. Initiates the handshake
def starttls_CDM(socket: socket, server_hostname: str) -> tuple[ssl.SSLSocket, str]:
    """Starts TLS command and either returns (none,server message) or a the ssl-interface for the socket and the server message"""

    # Ask for TLS/SSL capabilty by issuing starttls command
    socket.send("STARTTLS\r\n".encode())
    server_response = socket.recv(1024).decode()
    if server_response[:3] != '220':
        return (None, server_response)
    
    # # wait for server to be ready to start TLS/SSL handshake
    # server_response = socket.recv(1024).decode()
    # print(server_response)
    
    #create ssl socket
    # TODO: put in try catch block
    context = ssl.create_default_context()
    ssl_socket =  context.wrap_socket(socket,server_hostname=server_hostname)
    return (ssl_socket, server_response)