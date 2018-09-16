from socket import socket, AF_INET, SOCK_DGRAM

def ip():
    s = None
    res = 'unknown'
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        res = s.getsockname()[0]
    except:
        pass
    finally:
        if s: s.close()
    return res
