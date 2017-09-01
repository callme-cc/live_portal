# coding:utf-8

import MySQLdb

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='154625424',port=3306, charset='utf8')
    cur=conn.cursor()
    conn.select_db('live_portal')
    count=cur.execute('select * from live_rooms')
    print 'there has %s rows record' % count

    '''
    result=cur.fetchone()
    for i in result:
        print i
    #print 'ID: %s info %s' % result

    results=cur.fetchmany(5)
    for r in results:
        print r

    print '=='*10
    cur.scroll(0,mode='absolute')
    '''

    results=cur.fetchall()
    values=[]
    for idx,r in enumerate(results):
        v = list(r)
        v.insert(0,idx+1)
        values.append(v)
        print v

    cur.executemany('insert into live_portal_room values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',values)

    conn.commit()
    cur.close()
    conn.close()

except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
