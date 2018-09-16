import sys
import mysql.connector
import subprocess
import os

conn = None
def init():
    global conn
    conn = mysql.connector.connect(
            host = os.environ.get('DB_HOST'),
            user = os.environ.get('DB_USER'),
            password = os.environ.get('DB_PASS'),
            db = 'profile'
            )
    pass


def get_commit():
    return subprocess.check_output('git rev-parse HEAD', shell=True).strip()
def get_hostname():
    return subprocess.check_output('hostname', shell=True).strip()


def create_profile():
    if conn:
        cur = conn.cursor()
        commit_id = get_commit()
        hostname = get_hostname()
        sql = 'insert into profile (`commit_id`, `hostname`) VALUES (%s, %s)'
        cur.execute(sql, (commit_id, hostname))
        idx = cur.lastrowid
        cur.close()
        return idx
    else:
        return None

def insert_entry(routine, profile_id):
    if conn:
        cur = conn.cursor()
        print(routine['ratio'])
        sql = 'insert into cpuprofile (`profile_id`, `ratio`, `func_name`, `body`) VALUES (%s,%s,%s,%s)'
        cur.execute(sql, (profile_id, routine['ratio'], routine['name'], routine['body']))
        cur.close()

def doit(f):
    res = []
    total = None
    buf = []
    routine = {}
    profile_id = create_profile()
    
    while True:
        line = f.readline()
        if line == '': # EOF
            if routine:
                routine['body'] = ''.join(buf)
                res.append(routine)
            break
        if line.startswith('Total:'):
            total = line.split(':')[1].strip()
        elif line.startswith("ROUTINE"):
            if routine:
                routine['body'] = ''.join(buf)
                res.append(routine)
                routine = {}
                buf = []
            nline = f.readline()
            buf.append(nline)
            nline = nline.strip()
            funcname = line.split("========================")[1].strip()
            percentage = float(nline.split()[4][:-1])
            routine['name'] = funcname
            routine['ratio'] = percentage
        else:
            # remove line number
            end =  line.find(':')
            begin = line.rfind(' ',0,end)
            while begin >= 1 and line[begin-1] == ' ':
                begin -= 1
            line = line[:begin] + line[end+1:]    
            buf.append(line)

    # res.sort(key=lambda e: -e['ratio'])
    for routine in res:
        print ("ratio", routine['ratio'], '%')
        print ("name", routine['name'])
        print(routine['body'])
        insert_entry(routine, profile_id)
    if conn:
        conn.commit()

if __name__ == "__main__":
    init()
    doit(sys.stdin)
