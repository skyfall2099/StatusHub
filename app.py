from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
import yaml
import time
from datetime import datetime
from app.deployer import deploy_agent
from app.scheduler import scheduler
from app.data_manager import data_manager
from app.alert_manager import alert_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_key'

# 数据存储路径
DATA_DIR = 'data'
SERVERS_DIR = os.path.join(DATA_DIR, 'servers')
MONITORING_DIR = os.path.join(DATA_DIR, 'monitoring')
AGENTS_DIR = os.path.join(DATA_DIR, 'agents')
ALERTS_DIR = os.path.join(DATA_DIR, 'alerts')
AGENTS_SCRIPTS_DIR = 'agents'

# 确保目录存在
os.makedirs(SERVERS_DIR, exist_ok=True)
os.makedirs(MONITORING_DIR, exist_ok=True)
os.makedirs(AGENTS_DIR, exist_ok=True)
os.makedirs(ALERTS_DIR, exist_ok=True)
os.makedirs(AGENTS_SCRIPTS_DIR, exist_ok=True)

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 服务器管理
@app.route('/servers')
def servers():
    servers_list = data_manager.get_servers()
    return render_template('servers.html', servers=servers_list)

# 添加服务器
@app.route('/add_server', methods=['GET', 'POST'])
def add_server():
    if request.method == 'POST':
        server_data = {
            'name': request.form['name'],
            'ip': request.form['ip'],
            'port': int(request.form['port']),
            'username': request.form['username'],
            'password': request.form['password'],
            'status': 'offline',
            'last_heartbeat': datetime.now().isoformat()
        }
        data_manager.save_server(server_data)
        return redirect(url_for('servers'))
    return render_template('add_server.html')

# 编辑服务器
@app.route('/edit_server/<server_id>', methods=['GET', 'POST'])
def edit_server(server_id):
    server_info = data_manager.get_server(server_id)
    if not server_info:
        return redirect(url_for('servers'))
    
    if request.method == 'POST':
        server_info['name'] = request.form['name']
        server_info['ip'] = request.form['ip']
        server_info['port'] = int(request.form['port'])
        server_info['username'] = request.form['username']
        if request.form['password']:
            server_info['password'] = request.form['password']
        data_manager.save_server(server_info)
        return redirect(url_for('servers'))
    
    return render_template('edit_server.html', server=server_info)

# 删除服务器
@app.route('/delete_server/<server_id>')
def delete_server(server_id):
    data_manager.delete_server(server_id)
    return redirect(url_for('servers'))

# 监控工具管理
@app.route('/agents')
def agents():
    agents_list = []
    for file in os.listdir(AGENTS_SCRIPTS_DIR):
        if file.endswith('.py'):
            agents_list.append(file)
    return render_template('agents.html', agents=agents_list)

# 部署管理
@app.route('/deploy')
def deploy():
    servers_list = data_manager.get_servers()
    
    agents_list = []
    for file in os.listdir(AGENTS_SCRIPTS_DIR):
        if file.endswith('.py'):
            agents_list.append(file)
    
    return render_template('deploy.html', servers=servers_list, agents=agents_list)

# 部署Agent
@app.route('/deploy_agent', methods=['POST'])
def deploy_agent_route():
    server_id = request.form['server']
    agent_script = request.form['agent']
    schedule = request.form['schedule']
    
    # 加载服务器信息
    server_info = data_manager.get_server(server_id)
    if not server_info:
        return jsonify({"status": "error", "message": "服务器不存在"})
    
    # 部署Agent
    success, message = deploy_agent(server_info, agent_script, schedule)
    
    return jsonify({"status": "success" if success else "error", "message": message})

# 接收监控数据
@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "无数据"})
    
    # 提取服务器信息
    hostname = data.get('hostname', 'unknown')
    
    # 查找对应的服务器
    servers = data_manager.get_servers()
    server_id = servers[0]['id'] if servers else None
    
    if server_id:
        # 存储监控数据
        data_type = data.get('type', 'general')
        data_manager.save_monitoring_data(server_id, data_type, data)
        
        # 检查阈值并创建告警
        alert_manager.check_thresholds(server_id, data_type, data)
        
        # 更新服务器心跳
        server_info = data_manager.get_server(server_id)
        server_info['status'] = 'online'
        server_info['last_heartbeat'] = datetime.now().isoformat()
        data_manager.save_server(server_info)
    
    return jsonify({"status": "success"})

# 心跳检测
@app.route('/api/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    hostname = data.get('hostname', 'unknown')
    
    # 查找对应的服务器
    servers = data_manager.get_servers()
    server_id = servers[0]['id'] if servers else None
    
    if server_id:
        # 更新服务器心跳
        server_info = data_manager.get_server(server_id)
        server_info['status'] = 'online'
        server_info['last_heartbeat'] = datetime.now().isoformat()
        data_manager.save_server(server_info)
    
    return jsonify({"status": "success"})

# Dashboard
@app.route('/dashboard')
def dashboard():
    # 加载服务器数据
    servers_list = data_manager.get_servers()
    
    # 加载监控数据
    monitoring_data = {}
    for server in servers_list:
        server_data = data_manager.get_monitoring_data(server['id'])
        monitoring_data[server['id']] = server_data
    
    return render_template('dashboard.html', servers=servers_list, monitoring_data=monitoring_data)

# 告警管理
@app.route('/alerts')
def alerts():
    active_alerts = alert_manager.get_active_alerts()
    return render_template('alerts.html', alerts=active_alerts)

# 解决告警
@app.route('/resolve_alert/<alert_id>')
def resolve_alert(alert_id):
    alert_manager.resolve_alert(alert_id)
    return redirect(url_for('alerts'))

# 定期检查服务器状态
def check_servers_status():
    """检查服务器状态"""
    servers = data_manager.get_servers()
    for server in servers:
        # 检查最后心跳时间
        last_heartbeat = datetime.fromisoformat(server['last_heartbeat'])
        now = datetime.now()
        time_diff = (now - last_heartbeat).total_seconds()
        
        # 如果超过5分钟没有心跳，标记为离线
        if time_diff > 300 and server['status'] == 'online':
            server['status'] = 'offline'
            data_manager.save_server(server)

# 初始化调度器
def init_scheduler():
    """初始化调度器"""
    # 添加服务器状态检查任务，每1分钟执行一次
    scheduler.add_job(
        func=check_servers_status,
        trigger='interval',
        minutes=1,
        id='check_servers_status'
    )

if __name__ == '__main__':
    # 初始化调度器
    init_scheduler()
    app.run(debug=True, host='0.0.0.0', port=5000)