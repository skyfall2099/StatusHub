#!/usr/bin/env python3
import json
import time
import socket
import requests
import yaml
import os

class AgentBase:
    def __init__(self, config_file=None):
        self.config = {}
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        
        self.hostname = socket.gethostname()
        self.server_url = self.config.get('server_url', 'http://localhost:5000')
    
    def collect_data(self):
        """采集数据，子类需要实现"""
        raise NotImplementedError
    
    def send_data(self, data):
        """发送数据到主服务"""
        try:
            # 添加类型和主机名
            data['type'] = self.__class__.__name__.replace('Agent', '').lower()
            data['hostname'] = self.hostname
            
            # 发送数据
            response = requests.post(
                f"{self.server_url}/api/data",
                json=data,
                timeout=10
            )
            return response.status_code
        except Exception as e:
            print(f"发送数据失败: {e}")
            return None
    
    def send_heartbeat(self):
        """发送心跳"""
        try:
            response = requests.post(
                f"{self.server_url}/api/heartbeat",
                json={"hostname": self.hostname},
                timeout=5
            )
            return response.status_code
        except Exception as e:
            print(f"发送心跳失败: {e}")
            return None
    
    def run(self):
        """运行Agent"""
        # 发送心跳
        self.send_heartbeat()
        
        # 采集数据
        data = self.collect_data()
        
        # 发送数据
        if data:
            self.send_data(data)
        
        return data
    
    def get_metadata(self):
        """获取Agent元数据"""
        return {
            "name": self.config.get('name', self.__class__.__name__),
            "version": self.config.get('metadata', {}).get('version', '1.0'),
            "description": self.config.get('metadata', {}).get('description', ''),
            "hostname": self.hostname
        }

if __name__ == "__main__":
    # 测试基础Agent
    agent = AgentBase()
    print("Agent metadata:", agent.get_metadata())
    print("Sending heartbeat...")
    agent.send_heartbeat()