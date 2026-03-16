#!/usr/bin/env python3
import psutil
import json
import time
from agent_base import AgentBase

class NetworkAgent(AgentBase):
    def collect_data(self):
        """采集网络数据"""
        net_io = psutil.net_io_counters()
        net_connections = psutil.net_connections()
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        # 统计连接数
        connections_count = {
            'total': len(net_connections),
            'established': sum(1 for conn in net_connections if conn.status == 'ESTABLISHED'),
            'listen': sum(1 for conn in net_connections if conn.status == 'LISTEN'),
            'close_wait': sum(1 for conn in net_connections if conn.status == 'CLOSE_WAIT')
        }
        
        # 网络接口信息
        interfaces = {}
        for interface, addrs in net_if_addrs.items():
            if interface in net_if_stats:
                stats = net_if_stats[interface]
                interfaces[interface] = {
                    'isup': stats.isup,
                    'speed': stats.speed,
                    'mtu': stats.mtu
                }
        
        data = {
            "timestamp": time.time(),
            "net_io": {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout
            },
            "connections": connections_count,
            "interfaces": interfaces
        }
        
        return data

def main():
    """主函数"""
    agent = NetworkAgent()
    data = agent.run()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()