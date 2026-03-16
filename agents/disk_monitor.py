#!/usr/bin/env python3
import psutil
import json
import time
from agent_base import AgentBase

class DiskAgent(AgentBase):
    def collect_data(self):
        """采集磁盘数据"""
        disk_usage = psutil.disk_usage('/')
        disk_partitions = psutil.disk_partitions()
        
        partitions = []
        for partition in disk_partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "opts": partition.opts,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                })
            except:
                pass
        
        data = {
            "timestamp": time.time(),
            "disk_usage": {
                "total": disk_usage.total,
                "used": disk_usage.used,
                "free": disk_usage.free,
                "percent": disk_usage.percent
            },
            "partitions": partitions
        }
        
        return data

def main():
    """主函数"""
    agent = DiskAgent()
    data = agent.run()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()