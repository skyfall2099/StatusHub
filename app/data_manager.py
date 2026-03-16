import os
import json
import yaml
from datetime import datetime

class DataManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.servers_dir = os.path.join(data_dir, 'servers')
        self.monitoring_dir = os.path.join(data_dir, 'monitoring')
        self.agents_dir = os.path.join(data_dir, 'agents')
        self.alerts_dir = os.path.join(data_dir, 'alerts')
        
        # 确保目录存在
        os.makedirs(self.servers_dir, exist_ok=True)
        os.makedirs(self.monitoring_dir, exist_ok=True)
        os.makedirs(self.agents_dir, exist_ok=True)
        os.makedirs(self.alerts_dir, exist_ok=True)
    
    # 服务器管理
    def get_servers(self):
        """获取所有服务器"""
        servers = []
        for file in os.listdir(self.servers_dir):
            if file.endswith('.json'):
                with open(os.path.join(self.servers_dir, file), 'r') as f:
                    servers.append(json.load(f))
        return servers
    
    def get_server(self, server_id):
        """获取单个服务器"""
        server_file = os.path.join(self.servers_dir, f"{server_id}.json")
        if os.path.exists(server_file):
            with open(server_file, 'r') as f:
                return json.load(f)
        return None
    
    def save_server(self, server_data):
        """保存服务器信息"""
        server_id = server_data.get('id')
        if not server_id:
            server_id = f'server_{int(datetime.now().timestamp())}'
            server_data['id'] = server_id
        
        server_file = os.path.join(self.servers_dir, f"{server_id}.json")
        with open(server_file, 'w') as f:
            json.dump(server_data, f, indent=2)
        return server_id
    
    def delete_server(self, server_id):
        """删除服务器"""
        server_file = os.path.join(self.servers_dir, f"{server_id}.json")
        if os.path.exists(server_file):
            os.remove(server_file)
            return True
        return False
    
    # 监控数据管理
    def save_monitoring_data(self, server_id, data_type, data):
        """保存监控数据"""
        server_monitoring_dir = os.path.join(self.monitoring_dir, server_id)
        os.makedirs(server_monitoring_dir, exist_ok=True)
        
        data_file = os.path.join(server_monitoring_dir, f"{data_type}.json")
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_monitoring_data(self, server_id, data_type=None):
        """获取监控数据"""
        server_monitoring_dir = os.path.join(self.monitoring_dir, server_id)
        if not os.path.exists(server_monitoring_dir):
            return {}
        
        data = {}
        if data_type:
            data_file = os.path.join(server_monitoring_dir, f"{data_type}.json")
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data[data_type] = json.load(f)
        else:
            for file in os.listdir(server_monitoring_dir):
                if file.endswith('.json'):
                    data_type = file[:-5]
                    with open(os.path.join(server_monitoring_dir, file), 'r') as f:
                        data[data_type] = json.load(f)
        
        return data
    
    # Agent配置管理
    def save_agent_config(self, agent_id, config):
        """保存Agent配置"""
        config_file = os.path.join(self.agents_dir, f"{agent_id}.yaml")
        with open(config_file, 'w') as f:
            yaml.dump(config, f)
    
    def get_agent_config(self, agent_id):
        """获取Agent配置"""
        config_file = os.path.join(self.agents_dir, f"{agent_id}.yaml")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        return None
    
    # 告警管理
    def save_alert(self, alert_data):
        """保存告警"""
        alerts_file = os.path.join(self.alerts_dir, 'active_alerts.json')
        
        alerts = []
        if os.path.exists(alerts_file):
            with open(alerts_file, 'r') as f:
                alerts = json.load(f)
        
        alert_id = f'alert_{int(datetime.now().timestamp())}'
        alert_data['id'] = alert_id
        alert_data['timestamp'] = datetime.now().isoformat()
        alert_data['status'] = 'active'
        
        alerts.append(alert_data)
        
        with open(alerts_file, 'w') as f:
            json.dump(alerts, f, indent=2)
        
        return alert_id
    
    def get_active_alerts(self):
        """获取活跃告警"""
        alerts_file = os.path.join(self.alerts_dir, 'active_alerts.json')
        if os.path.exists(alerts_file):
            with open(alerts_file, 'r') as f:
                return json.load(f)
        return []
    
    def resolve_alert(self, alert_id):
        """解决告警"""
        alerts_file = os.path.join(self.alerts_dir, 'active_alerts.json')
        if not os.path.exists(alerts_file):
            return False
        
        with open(alerts_file, 'r') as f:
            alerts = json.load(f)
        
        updated = False
        for alert in alerts:
            if alert['id'] == alert_id:
                alert['status'] = 'resolved'
                alert['resolved_at'] = datetime.now().isoformat()
                updated = True
                break
        
        if updated:
            with open(alerts_file, 'w') as f:
                json.dump(alerts, f, indent=2)
        
        return updated

# 全局数据管理器实例
data_manager = DataManager()