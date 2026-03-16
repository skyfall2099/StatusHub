#!/usr/bin/env python3
import os
import re
import json
import time
from agent_base import AgentBase

class LogAgent(AgentBase):
    def collect_data(self):
        """采集日志数据"""
        # 监控的日志文件
        log_files = [
            '/var/log/syslog',
            '/var/log/auth.log'
        ]
        
        # 关键词列表
        keywords = ['error', 'warning', 'critical', 'fail', 'exception']
        
        log_stats = {}
        for log_file in log_files:
            if os.path.exists(log_file):
                keyword_counts = {}
                for keyword in keywords:
                    keyword_counts[keyword] = 0
                
                try:
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            for keyword in keywords:
                                if re.search(keyword, line, re.IGNORECASE):
                                    keyword_counts[keyword] += 1
                except:
                    pass
                
                log_stats[log_file] = keyword_counts
        
        data = {
            "timestamp": time.time(),
            "log_stats": log_stats
        }
        
        return data

def main():
    """主函数"""
    agent = LogAgent()
    data = agent.run()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()