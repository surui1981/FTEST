import subprocess
import re
import threading
import os
from datetime import datetime
import time

cwd = os.getcwd()

# Define the IP range of the current network segment
print("欢迎使用网络扫描工具！")
ip_range = input("请输入需要扫描的主机当前网段或目标网段用,号隔开例如 '192.168.1. ': ")
print("正在扫描，请稍等...")
# Define the function to ping an IP address
def ping(ip):
    result = subprocess.run(['ping', '-n', '1', '-w', '100', ip], stdout=subprocess.PIPE)
    output = result.stdout.decode('gbk')
    
    # Check if the ping was successful
    if re.search('TTL=', output):
        with lock:
            alive_hosts.append(ip)

# Loop over the possible IP addresses and ping each one using multiple threads
alive_hosts = []
lock = threading.Lock()  # Create a lock object
threads = []
start_time = time.time()

for i in range(1, 255):
    ip = ip_range + str(i)
    thread = threading.Thread(target=ping, args=(ip,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Get the current date and time
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 将当前工作目录路径和文件名拼接起来
file_path = os.path.join(cwd, 'alive_hosts.txt')

end_time = time.time()
elapsed_time = end_time - start_time

# Write the alive hosts and current date to a txt file
with open('alive_hosts.txt', 'w') as f:
    f.write(f"存活主机列表 (程序开始时间： {now}):\n 程序执行时间: {elapsed_time:.2f} 秒 \n ")
    for host in alive_hosts:
        f.write(host + '\n')

# Print the alive hosts
print("Alive hosts:")
for host in alive_hosts:
    print(host)

# Open the file
os.startfile(file_path)
