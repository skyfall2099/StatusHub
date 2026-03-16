#!/usr/bin/env python3
import os
import json
import time
from agent_base import AgentBase

class FileAgent(AgentBase):
    def collect_data(self):
        """采集文件数据"""
        # 监控的目录列表
        monitor_dirs = [
            '/var/log',
            '/tmp',
            '/home'
        ]
        
        dir_stats = {}
        for directory in monitor_dirs:
            if os.path.exists(directory):
                file_count = 0
                total_size = 0
                
                try:
                    for root, dirs, files in os.walk(directory):
                        file_count += len(files)
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                total_size += os.path.getsize(file_path)
                            except:
                                pass
                except:
                    pass
                
                dir_stats[directory] = {
                    'file_count': file_count,
                    'total_size': total_size
                }
        
        data = {
            "timestamp": time.time(),
            "directory_stats": dir_stats
        }
        
        return data

def main():
    """主函数"""
    agent = FileAgent()
    data = agent.run()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()