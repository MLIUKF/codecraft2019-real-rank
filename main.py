#coding=utf-8
import requests  
import os
import time

#各赛区排名url
urlList = ['https://codecraft.huawei.com:8843/preliminary/season/2/zone/1/pageIndex/1?timestamp=',\
        'https://codecraft.huawei.com:8843/preliminary/season/2/zone/2/pageIndex/1?timestamp=',\
        'https://codecraft.huawei.com:8843/preliminary/season/2/zone/3/pageIndex/1?timestamp=',\
        'https://codecraft.huawei.com:8843/preliminary/season/2/zone/4/pageIndex/1?timestamp=',\
        'https://codecraft.huawei.com:8843/preliminary/season/2/zone/5/pageIndex/1?timestamp=',\
        'https://codecraft.huawei.com:8843/preliminary/season/2/zone/6/pageIndex/1?timestamp',\
        'https://codecraft.huawei.com:8843/preliminary/season/2/zone/7/pageIndex/1?timestamp=',\
        'https://codecraft.huawei.com:8843/preliminary/season/2/zone/8/pageIndex/1?timestamp=']
#与url对应的地区名
zoneList = ['京津东北','上合','杭厦','江山','成渝','西北','武长','粤港澳']

if os.path.exists('teamInfo.txt'):
    with open('teamInfo.txt','r') as teamInfoFile:
        teamInfo = eval(teamInfoFile.read())
else:
    teamInfo = {'京津东北':dict(),'上合':dict(),'杭厦':dict(),'江山':dict(),'成渝':dict(),'西北':dict(),'武长':dict(),'粤港澳':dict()}

true = True    #由于python中未定义true，不先定义会出错
null = None     #同上
runOverTime = 9
#每分钟爬取一次，每五分钟保存一下文件，每十分钟更新一次排名
while True:
    for i in range(8):
        url = urlList[i] + str(int(time.time()*1000))
        dataDict = eval(requests.get(url).text)
        for team in dataDict['data']['dataList']:
            if team['teamName'] in teamInfo[zoneList[i]]:
                if int(team['finalScheduleTimeScore']) < int(teamInfo[zoneList[i]][team['teamName']]['finalScheduleTimeScore']):
                    teamInfo[zoneList[i]][team['teamName']]['finalScheduleTimeScore'] = team['finalScheduleTimeScore']
                    teamInfo[zoneList[i]][team['teamName']]['finalRunTimeScore'] = team['finalRunTimeScore']
                    teamInfo[zoneList[i]][team['teamName']]['finalAllScheduleScore'] = team['finalAllScheduleScore']
            else:
                teamInfo[zoneList[i]].update({team['teamName']:dict()})
                teamInfo[zoneList[i]][team['teamName']]['finalScheduleTimeScore'] = team['finalScheduleTimeScore']
                teamInfo[zoneList[i]][team['teamName']]['finalRunTimeScore'] = team['finalRunTimeScore']
                teamInfo[zoneList[i]][team['teamName']]['finalAllScheduleScore'] = team['finalAllScheduleScore']
                teamInfo[zoneList[i]][team['teamName']]['leader'] = team['leader']
                teamInfo[zoneList[i]][team['teamName']]['schoolName'] = team['schoolName']
                teamInfo[zoneList[i]][team['teamName']]['slogan'] = team['slogan']
    runOverTime += 1
    #保存文件
    if runOverTime%5 == 0:
        with open('teamInfo.txt','w') as teamInfoFile:
            teamInfoFile.write(str(teamInfo))
    #更新排名
    if runOverTime == 10:
        runOverTime = 0
        with open('rank.txt','w') as rankFile:
            rankFile.write(time.ctime()+'\n')
            rankFile.write('Rank Schedule Time  All Schedule Time Run Time       Team Name and SchoolName\n')
            for i in range(8):
                zone = zoneList[i]
                rankList = []
                for teamKey in teamInfo[zone]:
                    team = teamInfo[zone][teamKey]
                    rankList.append((int(team['finalScheduleTimeScore']),teamKey))
                rankList.sort()
                rankFile.write(zone+'\n')
                for rankNo,teamTuple in enumerate(rankList):
                    rankFile.write(str(rankNo+1).ljust(5,' '))
                    rankFile.write(str(teamTuple[0]).ljust(15,' '))
                    rankFile.write(teamInfo[zone][teamTuple[1]]['finalAllScheduleScore'].ljust(18,' '))
                    rankFile.write(teamInfo[zone][teamTuple[1]]['finalRunTimeScore'].ljust(15,' '))
                    rankFile.write(teamTuple[1]+'    ')
                    rankFile.write(teamInfo[zone][teamTuple[1]]['schoolName'])
                    rankFile.write('\n')
                rankFile.write('\n')
    time.sleep(60)