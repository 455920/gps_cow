# 1.导入模块
import socket
import threading
import json

temperature = ''
heart_rate = ''
pulse = ''
EW = ''# 东西
SN = '' # 南北
longitude = '' # 经度
latitude = '' # 纬度

# 储存参数的数组
arrs = []

def recv_msg(new_tcp_socket, ip_port):
    global arrs
    """
    接受信息的函数
    :return:
    """
    # 这个while可以不间断的接收客户端信息
    while True:
        # 7.接受客户端发送的信息
        recv_data = new_tcp_socket.recv(1024)
        if recv_data:
            # 8.解码数据并输出
            res_dict = {
                "code": "0",
                "arrs": ''
            }

            if recv_data == b'get':
               if len(arrs) == 0:
                   res_dict["code"] = "-1"
               else:
                   res_dict["arrs"] = arrs
               new_tcp_socket.sendall(json.dumps(res_dict).encode('utf8'))
            else:
                recv_text_utf8 = recv_data.decode('utf8')
                arrs = recv_text_utf8.split(',')


            recv_text = recv_data.decode('gbk')
            print('来自[%s]的信息：%s' % (str(ip_port), recv_text))
        else:
            break
    # 关闭客户端连接
    print('退出[%s]' % (str(ip_port)))
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
