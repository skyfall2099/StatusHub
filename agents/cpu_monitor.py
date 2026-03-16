#!/usr/bin/env python3
import psutil
import json
import time
from agent_base import AgentBase

class CpuAgent(AgentBase):
    def collect_data(self):
        """采集CPU数据"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_times = psutil.cpu_times()
        
        data = {
            "timestamp": time.time(),
            "cpu_percent": cpu_percent,
            "cpu_count": cpu_count,
            "cpu_times": {
                "user": cpu_times.user,
                "system": cpu_times.system,
                "idle": cpu_times.idle
            }
        }
        
        return data

def main():
    """主函数"""
    agent = CpuAgent()
    data = agent.run()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()