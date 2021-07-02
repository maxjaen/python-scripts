import os

ips = []

class Colors:
    BLUE = '\033[94m'
    FAIL = '\033[91m'

def print_with_color(color, text):
    print(f'{color}{text}')

def ip_available(ip):
        return os.system("ping -c 1 " + ip + " >/dev/null 2>&1") == 0;

if __name__ == "__main__":
    for ip in ips:
        ipAvailable = ip_available(ip)

        if ipAvailable:
            print_with_color(Colors.BLUE, f'IP {ip} available')
        else:
            print_with_color(Colors.FAIL, f'IP {ip} not available')
