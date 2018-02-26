#coding=utf-8
#Auther：noodles.huang
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeResourceUsageRequest,DescribeDBInstancePerformanceRequest,DescribeSlowLogRecordsRequest
import json,sys,datetime

ID = ''
Secret = ''
RegionId = 'ap-southeast-1'

clt = client.AcsClient(ID,Secret,RegionId)

Type = sys.argv[1]
DBInstanceId = sys.argv[2]
#Key = sys.argv[3]


UTC_End = datetime.datetime.today() - datetime.timedelta(hours=8) - datetime.timedelta(minutes=70)
UTC_Start = UTC_End - datetime.timedelta(minutes=5)

StartTime = datetime.datetime.strftime(UTC_Start, '%Y-%m-%dT%H:%MZ')
EndTime = datetime.datetime.strftime(UTC_End, '%Y-%m-%dT%H:%MZ')

print StartTime
print EndTime


def GetSlowlog(DBInstanceId,StartTime,EndTime):
    Slowlog = DescribeSlowLogRecordsRequest.DescribeSlowLogRecordsRequest()
    Slowlog.set_accept_format('json')
    Slowlog.set_DBInstanceId(DBInstanceId)
    Slowlog.set_StartTime(StartTime)
#    Slowlog.set_StartTime("2017-10-13T15:00Z")
    Slowlog.set_EndTime(EndTime)
    SlowlogInfo = clt.do_action_with_exception(Slowlog)
    Info = (json.loads(SlowlogInfo))
    PageRecordCount = Info['PageRecordCount']
#    print PageRecordCount
    if PageRecordCount == 0:
      print 0
    else:
    	i = 0
        while i < PageRecordCount:
        		SQL = Info['Items']['SQLSlowRecord'][i]['SQLText']
        		DBNAME = Info['Items']['SQLSlowRecord'][i]['DBName']
        		QueryTimes = Info['Items']['SQLSlowRecord'][i]['QueryTimes']
        		i = i + 1
        		print "No: %s ,DBNAME: %s ,QueryTimes: %s ,SLOWSQL: %s" % (i, DBNAME, QueryTimes, SQL)

if (Type == "Slowlog"):
        GetSlowlog(DBInstanceId,StartTime,EndTime)
