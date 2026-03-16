#!/usr/bin/env python3
import psutil
import json
import time
from agent_base import AgentBase

class MemoryAgent(AgentBase):
    def collect_data(self):
        """采集内存数据"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        data = {
            "timestamp": time.time(),
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent
            }
        }
        
        return data

def main():
    """主函数"""
    agent = MemoryAgent()
    data = agent.run()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()