import json
import os
from datetime import datetime
from app.data_manager import data_manager

class AlertManager:
    def __init__(self):
        # 告警阈值配置
        self.thresholds = {
            'cpu': {
                'warning': 70,  # 70% 警告
                'critical': 90  # 90% 严重
            },
            'disk': {
                'warning': 70,
                'critical': 90
            },
            'memory': {
                'warning': 70,
                'critical': 90
            }
        }
    
    def check_thresholds(self, server_id, data_type, data):
        """检查监控数据是否超过阈值"""
        if data_type not in self.thresholds:
            return
        
        thresholds = self.thresholds[data_type]
        
        # 根据数据类型获取相应的值
        if data_type == 'cpu':
            value = data.get('cpu_percent', 0)
        elif data_type == 'disk':
            value = data.get('disk_usage', {}).get('percent', 0)
        elif data_type == 'memory':
            value = data.get('memory', {}).get('percent', 0)
        else:
            return
        
        # 检查是否超过阈值
        if value >= thresholds['critical']:
            self.create_alert(server_id, data_type, 'critical', f"{data_type.upper()} usage is {value}%, which exceeds critical threshold of {thresholds['critical']}%")
        elif value >= thresholds['warning']:
            self.create_alert(server_id, data_type, 'warning', f"{data_type.upper()} usage is {value}%, which exceeds warning threshold of {thresholds['warning']}%")
    
    def create_alert(self, server_id, alert_type, level, message):
        """创建告警"""
        # 检查是否已经有相同的活跃告警
        active_alerts = data_manager.get_active_alerts()
        for alert in active_alerts:
            if (alert['server_id'] == server_id and 
                alert['type'] == alert_type and 
                alert['level'] == level and 
                alert['status'] == 'active'):
                # 已经存在相同的告警，不再创建
                return
        
        # 创建新告警
        alert_data = {
            'server_id': server_id,
            'type': alert_type,
            'level': level,
            'message': message
        }
        data_manager.save_alert(alert_data)
    
    def get_active_alerts(self):
        """获取活跃告警"""
        return data_manager.get_active_alerts()
    
    def resolve_alert(self, alert_id):
        """解决告警"""
        return data_manager.resolve_alert(alert_id)

# 全局告警管理器实例
alert_manager = AlertManager()