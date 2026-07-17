#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UDP NAT Type Tester - VPS端
功能：监听指定端口，收到任何数据后返回 PONG
"""

import socket

VPS_PORT = 55555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', VPS_PORT))

print(f"[VPS] UDP回声服务器启动，监听端口 {VPS_PORT}")
print(f"[VPS] 收到数据将回复 PONG from VPS")
print("-" * 50)

try:
    while True:
        data, addr = sock.recvfrom(1024)
        content = data.decode('utf-8', errors='ignore').strip()
        print(f"[VPS] 收到来自 {addr[0]}:{addr[1]} -> {content or '(空数据)'}")
        
        # 回复 PONG
        reply = b"PONG from VPS"
        sock.sendto(reply, addr)
        print(f"[VPS] 已回复 {addr[0]}:{addr[1]}")
except KeyboardInterrupt:
    print("\n[VPS] 用户中断，退出")
finally:
    sock.close()