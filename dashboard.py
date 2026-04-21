import streamlit as st
import paramiko

# Page config
st.set_page_config(
    page_title=" 📈 Network Automation Dashboard",
    page_icon="",
    layout="wide"
)

# Custom CSS for professional look
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
    color: #0a3d62;
}
h1, h2, h3 {
    color: #0a3d62;
}
.stButton>button {
    background-color: #0a3d62;
    color: white;
    height: 3em;
    width: 100%;
    border-radius: 10px;
}
.stTextInput>div>div>input {
    border-radius: 10px;
    padding: 10px;
}
.report-box {
    background-color: #dff9fb;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 6px solid #0a3d62;
}
</style>
""", unsafe_allow_html=True)

st.title(" 🌐 Network Automation Dashboard")
st.markdown("**Monitor Ubuntu Server in real-time with SSH**")

# Inputs
host = st.text_input("Enter Ubuntu IP", "10.230.129.187")
username = st.text_input("Username", "ubuntu")
password = st.text_input("Password", type="password")

if st.button("Connect and Monitor"):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password, timeout=5)

        commands = {
            "Hostname": "hostname",
            "IP Address": "ip a",
            "Open Ports": "ss -tulnp",
            "Memory Usage": "free -h",
            "Disk Usage": "df -h",
            "CPU Load": "uptime",
            "Ping Test": "ping -c 4 8.8.8.8",
        }

        # Display data in 2 columns for better UX
        col1, col2 = st.columns(2)

        for i, (title, cmd) in enumerate(commands.items()):
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()

            with (col1 if i % 2 == 0 else col2):
                st.markdown(f'<div class="report-box"><h3>{title}</h3><pre>{output}</pre></div>', unsafe_allow_html=True)

        ssh.close()

    except Exception as e:
        st.error(f"❌ Connection Failed: {e}")