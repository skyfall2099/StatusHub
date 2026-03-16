import paramiko
import os
import time

def deploy_agent(server_info, agent_script, schedule):
    """
    部署监控Agent到目标服务器
    :param server_info: 服务器信息字典
    :param agent_script: 监控脚本文件名
    :param schedule: cron表达式
    :return: 部署结果
    """
    try:
        # 创建SSH客户端
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接服务器
        client.connect(
            hostname=server_info['ip'],
            port=server_info['port'],
            username=server_info['username'],
            password=server_info['password']
        )
        
        # 创建监控目录
        agent_dir = '/opt/statushub/agents'
        stdin, stdout, stderr = client.exec_command(f'mkdir -p {agent_dir}')
        stdout.read()
        
        # 上传监控脚本
        sftp = client.open_sftp()
        local_script_path = os.path.join('agents', agent_script)
        remote_script_path = os.path.join(agent_dir, agent_script)
        sftp.put(local_script_path, remote_script_path)
        
        # 设置执行权限
        client.exec_command(f'chmod +x {remote_script_path}')
        
        # 创建配置文件
        config_content = f'''
id: {agent_script.replace('.py', '')}
name: {agent_script.replace('.py', '').replace('_', ' ').title()}
script: {agent_script}
schedule: "{schedule}"
parameters: {{}}
metadata:
  author: "StatusHub"
  version: "1.0"
  description: "{agent_script.replace('.py', '').replace('_', ' ').title()} Monitor"
'''
        config_file = agent_script.replace('.py', '.yaml')
        remote_config_path = os.path.join(agent_dir, config_file)
        with sftp.open(remote_config_path, 'w') as f:
            f.write(config_content)
        
        # 添加cron任务
        cron_command = f'*/5 * * * * python3 {remote_script_path} >> /var/log/statushub.log 2>&1'
        stdin, stdout, stderr = client.exec_command(f'(crontab -l 2>/dev/null; echo "{cron_command}") | crontab -')
        stdout.read()
        
        # 关闭连接
        sftp.close()
        client.close()
        
        return True, f"Agent {agent_script} 部署成功"
        
    except Exception as e:
        return False, f"部署失败: {str(e)}"

def test_connection(server_info):
    """
    测试服务器连接
    :param server_info: 服务器信息字典
    :return: 连接结果
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=server_info['ip'],
            port=server_info['port'],
            username=server_info['username'],
            password=server_info['password'],
            timeout=5
        )
        client.close()
        return True, "连接成功"
    except Exception as e:
        return False, f"连接失败: {str(e)}"