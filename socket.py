import socket
import fcntl
import struct

def get_ip_addr(ifname):
    # AF_INET IPv4プロトコルを使用する
    # SOCKE_DGRAM: UDPを用いる
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # inet_ntoa: 32ビットのパックしたバイナリ形式のアドレスをドット記法の文字列に変換する
    ip = socket.inet_ntoa(fcntl.ioctl(
        # ソケットのファイルディスクリプタの整数
        s.fileno(),
        # SIOCGIFADDR
        0x8915,
        # 256s > 256 bytesに変換
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])

    s.close()

    return ip

def get_mac_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mac = fcntl.ioctl(
        s.fileno(),
        0x8927,
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[18:24]
    s.close()

    return ':'.join(['{:02x}'.format(char) for char in mac])

def get_ipaddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.connect(("8.8.8.8", 53))
    addr = s.getsockname()
    s.close()
    return addr[0]

if __name__ == "__main__":
    print(get_ip_addr('enp3s0'))
    print(get_mac_addr('enp3s0'))
    print(get_ipaddress())
