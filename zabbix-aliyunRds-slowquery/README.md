# zabbix-RDS-monitor
Aliyun RDS-mysql status monitor with zabbix   
   
zabbix通过阿里云api 自动发现、监控阿里云RDS-Mysql慢查询日志报警     
## 使用方法
### 注意事项
1. 脚本会收集RDS别名，
2. 不要默认别名
3. 不要使用中文别名（zabbix不识别）
4. 切记aliyun-python-sdk-core==2.3.5，新版本的sdk有bug
### 环境要求
python = 2.7
### 模块安装
```shell
pip install aliyun-python-sdk-core==2.3.5 aliyun-python-sdk-rds datetime
```
### 使用方法
1. 从阿里云控制台获取 **AccessKey** ,并修改脚本中的 **ID** 与 **Secret**
2. 修改区域 **RegionId**
3. 将两个脚本放置于以下目录
```conf
/etc/zabbix/script
```
```shell
chmod +x /etc/zabbix/script/*
```
4. /etc/zabbix/zabbix_agentd.d/userparameter_aliyunRDSslowquery.conf
UserParameter=rds.find,python /etc/zabbix/script/discovery_rds.py
UserParameter=aliyun.rds.slow[*],python /etc/zabbix/script/aliyun_rds_slowlog.py Slowlog $1
```
5. 重启zabbix-agent
6. zabbix控制台导入模板，并关联主机
