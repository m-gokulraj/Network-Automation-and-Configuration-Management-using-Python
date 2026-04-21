import paramiko
from datetime import datetime

host = "10.230.129.187"
username = "ubuntu"
password = "ubuntu"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("Connecting...")

ssh.connect(host, username=username, password=password)

commands = {
    "Hostname": "hostname",
    "IP Address": "ip a",
    "Open Ports": "ss -tulnp",
    "Memory Usage": "free -h",
    "Disk Usage": "df -h",
    "CPU Load": "uptime",
    "Ping Test": "ping -c 4 8.8.8.8"
}

report = f"===== SYSTEM REPORT =====\nTime: {datetime.now()}\n\n"

for title, cmd in commands.items():
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()

    print(f"\n=== {title} ===")
    print(output)

    report += f"\n=== {title} ===\n{output}\n"

filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(filename, "w") as f:
    f.write(report)

ssh.close()

print(f"\n✅ Report saved as {filename}")