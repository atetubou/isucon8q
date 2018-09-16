from flask import Flask,render_template, request
import mysql.connector
import os, sys
import tempfile
import difflib

import mysql.connector 

app = Flask(__name__)
dbconfig = {
    "database" : 'profile',
    "user" : os.environ['DB_USER'],
    "password" : os.environ['DB_PASS'],
    "host" : os.environ['DB_HOST'],  
    "pool_name" : "mysql_pool",
    "pool_size" : 20,
    "charset": 'utf8mb4',
    "autocommit" : True
}

def get_connection():
    return mysql.connector.connect(**dbconfig)

def get_profile(conn, rev_id, hostname):
    cur = conn.cursor(dictionary=True)
    try: 
        sql = 'select * from profile where commit_id like %s AND hostname = %s order by created_at desc limit 1'
        cur.execute(sql, (rev_id + '%', hostname))
        entry = cur.fetchone()
        if not entry:
            return None
        profile_id = entry['id']
        sql = 'select * from cpuprofile where profile_id = %s'
        cur.execute(sql, (profile_id,))
        res = [ { 'func_name' : row['func_name'].decode('utf8'),
                  'ratio' : row['ratio'],
                  'body' : row['body'].decode('utf8')} for row in cur ]
        return res
    finally:
        cur.close()
def compare_profile(profile1, profile2):
    keys = set()
    tbl1 = {}
    tbl2 = {}
    for routine in profile1:
        keys.add(routine['func_name'])
        tbl1[routine['func_name']] = routine
    for routine in profile2:
        keys.add(routine['func_name'])
        tbl2[routine['func_name']] = routine
    ret = []
    for key in keys:
        res = [tbl1.get(key,{}),tbl2.get(key,{})]
        body1 = list(map(lambda l: l , res[0].get('body','').split('\n')))
        body2 = list(map(lambda l: l , res[1].get('body','').split('\n')))
        diffHTML = difflib.HtmlDiff().make_table(body1, body2, context=True, numlines=1)
        ratio = res[0].get('ratio', res[1].get('ratio',0))
        ret.append({ 'func_name' : key, 
                     'ratio': ratio, 
                     'diffHTML' :diffHTML})
    ret.sort(key=lambda e: -e['ratio'])
    return ret

def commit_list(conn):
    cur = conn.cursor(dictionary=True)
    try: 
        cur.execute('select commit_id from profile group by commit_id order by MAX(created_at) desc limit 10')
        res = list(row['commit_id'].decode('utf8')[:10] for row in cur)
        return res
    finally:
        cur.close()

def hostname_list(conn):
    cur = conn.cursor(dictionary=True)
    try: 
        cur.execute('select hostname from profile group by hostname')
        res = list(row['hostname'].decode('utf8') for row in cur)
        return res
    finally:
        cur.close()


@app.route("/")
def index():
    conn = get_connection()
    try:
        commits = commit_list(conn)
        hosts = hostname_list(conn)
        rev_id1 = request.args.get('rev_id1')
        rev_id2 = request.args.get('rev_id2')
        host1 = request.args.get('hostname1')
        host2 = request.args.get('hostname2')
        comp = None
        profile1 = None
        if rev_id1 and host1:
            if rev_id2 and host2:
                profile1 = get_profile(conn, rev_id1, host1)
                profile2 = get_profile(conn, rev_id2, host2)
                comp = compare_profile(profile1, profile2)
            else:
                profile1 = get_profile(conn, rev_id1, host1)
                profile1.sort(key = lambda e: -e['ratio'])
    finally:
        conn.close()

    return render_template('index.html', 
            commits = commits,
            hosts = hosts,
            profile1 = profile1,
            comp = comp)

if __name__ == "__main__":
    app.run(debug=True)
