from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import json
from datetime import datetime

class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
    
    def add_job(self, func, trigger, id, **kwargs):
        """添加任务"""
        self.scheduler.add_job(
            func=func,
            trigger=trigger,
            id=id,
            replace_existing=True,
            **kwargs
        )
    
    def remove_job(self, id):
        """移除任务"""
        try:
            self.scheduler.remove_job(id)
            return True
        except:
            return False
    
    def get_jobs(self):
        """获取所有任务"""
        return self.scheduler.get_jobs()
    
    def shutdown(self):
        """关闭调度器"""
        self.scheduler.shutdown()

# 全局调度器实例
scheduler = Scheduler()

# 示例任务函数
def sample_task():
    print(f"任务执行时间: {datetime.now()}")
    # 这里可以添加实际的任务逻辑

# 初始化调度器
# scheduler.add_job(
#     func=sample_task,
#     trigger=CronTrigger(minute='*/5'),  # 每5分钟执行一次
#     id='sample_task'
# )