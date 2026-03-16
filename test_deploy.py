#!/usr/bin/env python3
"""
测试部署功能
"""
import json
import os
from app.deployer import deploy_agent, test_connection

# 测试服务器信息
server_info = {
    'id': 'test_server',
    'name': 'Test Server',
    'ip': '127.0.0.1',  # 替换为实际服务器IP
    'port': 22,
    'username': 'root',  # 替换为实际用户名
    'password': 'password'  # 替换为实际密码
}

# 测试连接
def test_server_connection():
    print("测试服务器连接...")
    success, message = test_connection(server_info)
    print(f"连接结果: {success}, 消息: {message}")

# 测试部署
def test_agent_deployment():
    print("测试部署Agent...")
    agent_script = 'cpu_monitor.py'
    schedule = '*/5 * * * *'
    success, message = deploy_agent(server_info, agent_script, schedule)
    print(f"部署结果: {success}, 消息: {message}")

if __name__ == "__main__":
    test_server_connection()
    # 测试部署前请确保服务器信息正确
    # test_agent_deployment()