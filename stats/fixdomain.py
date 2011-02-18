__author__ = 'fearless'

import re
from statsutils import replace_nonascii
from statsdb import db_open, db_close

cc = db_open()
c = cc[0]
conn = cc[1]

c.execute("SELECT id, action FROM wp_bp_activity")
activities = c.fetchall()

for activity in activities:
    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', activity[1])
    if ip:
        print ip
        new_action = activity[1].replace(ip[0], "")
        sql = "UPDATE wp_bp_activity SET action = '%s' WHERE id = %d" % (replace_nonascii(new_action), int(activity[0]))
        print sql
        c.execute(sql)
db_close(c, conn)
