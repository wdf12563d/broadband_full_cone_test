#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UDP NAT Type Tester - Windows端
功能：绑定本地端口，持续向VPS发包维持会话，同时监听所有进入的数据包
"""

import socket
import time
import threading

# ============ 配置区 ============
LOCAL_PORT = 55555          # 本地监听端口
VPS_IP = "Your ip"     # 你的VPS公网IP
VPS_PORT = 55555            # VPS端监听端口
# ================================

# 全局标志
keep_sending = True


def send_keepalive(sock, target_ip, target_port):
    """持续向VPS发送心跳包，维持CGN会话"""
    count = 0
    print("[发包线程] 启动，每2秒向VPS发送一次...")
    while keep_sending:
        count += 1
        msg = f"Keepalive #{count}".encode()
        sock.sendto(msg, (target_ip, target_port))
        print(f"[发包] #{count} -> VPS")
        time.sleep(2)


def listen(sock):
    """监听所有进入本地端口的数据包"""
    print("[监听线程] 启动，等待数据...")
    print("-" * 50)
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            content = data.decode('utf-8', errors='ignore').strip()
            if content:
                print(f"[收到] 来自 {addr[0]}:{addr[1]} -> {content}")
            else:
                print(f"[收到] 来自 {addr[0]}:{addr[1]} -> (空数据)")
        except Exception as e:
            print(f"[错误] {e}")


def main():
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', LOCAL_PORT))
    
    print(f"[系统] 本地端口 {LOCAL_PORT} 已绑定")
    print(f"[系统] 外层映射端口: 布吉岛")
    print(f"[系统] 公网IP: 不知道") #公网IP和端口可通过测试端获取
    print("-" * 50)

    # 启动持续发包线程
    sender_thread = threading.Thread(
        target=send_keepalive, 
        args=(sock, VPS_IP, VPS_PORT),
        daemon=True
    )
    sender_thread.start()

    # 主线程负责监听
    try:
        listen(sock)
    except KeyboardInterrupt:
        print("\n[系统] 用户中断，正在退出...")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
