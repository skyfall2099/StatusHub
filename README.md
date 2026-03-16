# StatusHub - 轻量级服务器监控系统

## 项目介绍
StatusHub是一个轻量级的服务器监控系统，使用Python开发，采用调度任务架构，主服务采集各个监控Agent返回的内容，展示在Dashboard上。

## 核心功能

### 1. 服务器管理
- 添加、编辑、删除服务器信息
- 存储服务器SSH连接信息

### 2. 监控工具管理
- 自动列出所有监控脚本（agents目录下的.py文件）
- 查看脚本内容
- 查看部署情况

### 3. 部署管理
- 选择监控脚本部署到目标服务器
- 配置cron调度任务
- 远程部署和执行

### 4. 监控数据采集
- CPU使用率监控
- 磁盘空间监控
- 内存使用率监控
- 网络流量监控
- 文件存在性监控
- 日志关键词监控

### 5. 数据可视化
- 实时Dashboard展示
- 环形图展示使用率
- 状态颜色指示

### 6. 告警系统
- 基于阈值的自动告警
- 告警状态管理

### 7. 心跳检测
- 定期检查服务器状态
- 确保Agent存活

## 技术栈
- Python 3.14+
- Flask（Web框架）
- APScheduler（任务调度）
- Paramiko（SSH连接）
- PyYAML（配置文件）
- psutil（系统监控）
- Chart.js（数据可视化）

## 安装步骤

1. 克隆仓库
   ```bash
   git clone https://github.com/skyfall2099/StatusHub
   cd StatusHub
   ```

2. 安装依赖
   ```bash
   python -m pip install -r requirements.txt
   ```

3. 启动服务
   ```bash
   python app.py
   ```

4. 访问系统
   打开浏览器访问：http://127.0.0.1:5000

## 目录结构

```
StatusHub/
├── app/              # 主服务代码
│   ├── data_manager.py       # 数据管理
│   ├── alert_manager.py      # 告警管理
│   ├── deployer.py           # 部署管理
│   └── scheduler.py          # 任务调度
├── agents/           # 监控脚本
│   ├── agent_base.py         # Agent基类
│   ├── cpu_monitor.py        # CPU监控
│   ├── disk_monitor.py       # 磁盘监控
│   ├── memory_monitor.py     # 内存监控
│   ├── network_monitor.py    # 网络监控
│   ├── file_monitor.py       # 文件监控
│   └── log_monitor.py        # 日志监控
├── data/             # 数据存储
├── static/           # 静态资源
├── templates/        # HTML模板
├── app.py            # 主应用入口
├── requirements.txt  # 依赖包
└── README.md        # 项目说明
```

## 使用说明

1. **添加服务器**：在"服务器管理"页面添加需要监控的服务器
2. **部署监控**：在"部署管理"页面选择监控脚本和目标服务器，配置调度任务
3. **查看状态**：在"Dashboard"页面查看服务器监控状态
4. **管理告警**：在"告警管理"页面查看和处理告警

## 注意事项

- 本系统为轻量级解决方案，使用文件存储数据，不依赖数据库
- 部署监控时需要确保目标服务器已安装Python和必要的依赖
- 建议在安全环境中使用，避免在公网暴露

## 扩展指南

要添加新的监控脚本，只需在`agents`目录下创建新的.py文件，继承`AgentBase`类并实现`collect_data`方法即可。

## 许可证

MIT License
