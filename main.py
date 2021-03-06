# -*- coding=utf-8 -*-
# 1.导入模块
import socket
import threading
import json
import datetime



# 储存参数的数组
# 0温度 1心率 2 脉搏  3经度 4纬度 5时间

# 储存牛的数据
# key:id  value: 生命体征
cows_data = {}

def recv_msg(new_tcp_socket, ip_port):
    global arrs
    recv_data = ''
    """
    接受信息的函数
    :return:
    """
    # 这个while可以不间断的接收客户端信息
    while True:
        # 7.接受客户端发送的信息
        ch = new_tcp_socket.recv(1)
        if ch != b'*':
            recv_data += ch.decode('utf8')
            continue

        if recv_data:
            # 8.解码数据并输出
            res_dict = {
                "code": "0",
                "cow_data": ''
            }

            recv_text_utf8 = recv_data

            req = recv_text_utf8.split(':')


            # 请求不合法
            if len(req) < 1:
                print('req params error')

            method = req[0]

            if method == 'get': # 请求格式 get:id
                # 请求不合法
                if len(req) != 2:
                    print('get params error')


                if req[1] in cows_data.keys(): # 判断id是否对应有数据
                    res_dict["cow_data"] = cows_data[req[1]]
                else:
                    res_dict["code"] = "-1" # 表示该牛不存在
                    res_dict["cow_data"] = []
                new_tcp_socket.sendall(json.dumps(res_dict).encode('utf8'))

            elif method == 'set':
                # 请求不合法
                if len(req) != 3:
                    print('set params error')


                cow_data = req[2].split(',')
                cow_data.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                cows_data[req[1]] = cow_data
            else: # 方法错误
                print('method params error')


            # recv_text = recv_data.decode('gbk')
            print(str(ip_port), recv_text_utf8)

            recv_data = ''
        else:
            print("recv_data error")
            break
    # 关闭客户端连接
    print('a client quit')
    new_tcp_socket.close()


# 2.创建套接字
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 3.设置地址可以重用
tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
# 4.绑定端口
tcp_server_socket.bind(("0.0.0.0", 8080))

# 5.设置监听，套接字由主动变为被动
tcp_server_socket.listen(128)

# 用一个while True来接受多个客户端连接
while True:
    # 6.接收客户端连接
    new_tcp_socket, ip_port = tcp_server_socket.accept()
    print('新用户[%s]连接' % str(ip_port))

    # 创建线程
    thread_msg = threading.Thread(target=recv_msg, args=(new_tcp_socket, ip_port))
    # 子线程守护主线程
    thread_msg.setDaemon(True)
    # 启动线程
    thread_msg.start()
    # 调用接收函数
    # recv_msg(new_tcp_socket, ip_port)

# tcp_server_socket.close()
