#coding=utf-8
#Auther：noodles.huang
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeSlowLogsRequest,DescribeResourceUsageRequest,DescribeDBInstancePerformanceRequest,DescribeSlowLogRecordsRequest
import json,sys,datetime

ID = ''
Secret = ''
RegionId = 'cn-'

clt = client.AcsClient(ID,Secret,RegionId)

Type = sys.argv[1]
DBInstanceId = sys.argv[2]
#Sortkey = sys.argv[3]
#Key = sys.argv[3]


UTC_End = datetime.datetime.today() - datetime.timedelta(hours=8) - datetime.timedelta(days=1)
UTC_Start = UTC_End - datetime.timedelta(days=7)

StartTime = datetime.datetime.strftime(UTC_Start, '%Y-%m-%dZ')
EndTime = datetime.datetime.strftime(UTC_End, '%Y-%m-%dZ')

#print StartTime
#print EndTime

print "Mysql实例:%s 慢查询报表统计时间段: %s - %s" % (DBInstanceId, StartTime, EndTime)

def GetSlowlog(DBInstanceId,StartTime,EndTime):
    Slowlog = DescribeSlowLogsRequest.DescribeSlowLogsRequest()
    Slowlog.set_accept_format('json')
    Slowlog.set_DBInstanceId(DBInstanceId)
    Slowlog.set_StartTime(StartTime)
    Slowlog.set_PageSize(100)
#    Slowlog.set_SortKey(Sortkey)
#    Slowlog.set_StartTime("2017-10-13T15:00Z")
    Slowlog.set_EndTime(EndTime)
    SlowlogInfo = clt.do_action_with_exception(Slowlog)
    Info = (json.loads(SlowlogInfo))
#    print Info
    PageRecordCount = Info['PageRecordCount']
#    print PageRecordCount
    if PageRecordCount == 0:
      print 0
    else:
    	i = 0
        while i < PageRecordCount:
        		SQL = Info['Items']['SQLSlowLog'][i]['SQLText']
        		DBNAME = Info['Items']['SQLSlowLog'][i]['DBName']
        		ExecutionCounts = Info['Items']['SQLSlowLog'][i]['MySQLTotalExecutionCounts']
                        MaxExecutionTime = Info['Items']['SQLSlowLog'][i]['MaxExecutionTime']
        		MySQLTotalExecutionTimes = Info['Items']['SQLSlowLog'][i]['MySQLTotalExecutionTimes']
                        i = i + 1
        		print "No: %s ,DBNAME: %s ,ExecutionCounts: %s ,MaxExecutionTime: %s ,MySQLTotalExecutionTimes: %s ,SLOWSQL: %s" % (i, DBNAME, MaxExecutionTime, ExecutionCounts, MySQLTotalExecutionTimes, SQL)

if (Type == "Slowlog"):
        GetSlowlog(DBInstanceId,StartTime,EndTime)
