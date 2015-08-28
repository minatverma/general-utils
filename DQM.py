import os
import sys
import pandas as pd
import pyodbc
from pandas.util.testing import assert_frame_equal
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def dqm_newark() :
    conn_nwk = create_connection_nwk()
    dataframes_newark = []
    tgtfile = open('tgtqueries.sql', 'rU').read()
    querylist = tgtfile.split(';')
    querylist.pop()
    for query in querylist :
        dataframes_newark.append(pd.read_sql(query, conn_nwk))
    close_connection(conn_nwk)
    return dataframes_newark

def dqm_redwood() :
    conn_rw = create_connection_redwood()
    dataframes_redwood = []
    srcfile = open('srcqueries.sql', 'rU').read()
    querylist = srcfile.split(';')
    querylist.pop()
    for query in querylist :
        dataframes_redwood.append(pd.read_sql(query, conn_rw))
    close_connection(conn_rw)
    return dataframes_redwood

def compare_data():
    HEADER = '''
    <html>
    <head>
        <style>
            .df{
                  width: 100%;
                  margin-bottom: 15px;
                  border: 1px solid #ececec;
                  font-family: helvetica neue;
              }
            .df td,.df th{
              border: none;
              padding: 5px;
              text-align: center;
            }
            .df thead th {    
                background-color: #ececec;
                color: #333;
                font-weight: 400;
                font-size: 14px;
            }
            .df tbody td,.df tbody th {
                color: #333;
                font-weight: 400;
                font-size: 12px;
            }
            .df tr:nth-child(even) {background: #ececec}
            .df tr:nth-child(odd) {background: #FFF}

            .df thead th:nth-child(1),.df tbody th:nth-child(1){
              width:20%;
            }
            
            .df th:nth-child(2),.df th:nth-child(3),
            .df td:nth-child(2),.df td:nth-child(3){
              width:40%;
            }
        </style>
    </head>
    <body>
    '''
    FOOTER = '''
    </body>
    </html>
    '''
    html_out = open('test.html', 'a')
    print "Cross DB validaiton Starts :"
    try:
      src_dataframes = dqm_redwood()
      tgt_dataframes = dqm_newark()
      html_out.write(HEADER)
      for i in xrange(len(src_dataframes)):
          html_out.write(src_dataframes[i].to_html(classes='df'))
          html_out.write(tgt_dataframes[i].to_html(classes='df'))
          assert_frame_equal(src_dataframes[i], tgt_dataframes[i],check_names=False)
      print 'Data Matches'
      html_out.write(FOOTER)
    except:
      print 'Nopes !!'
      print sys.exc_info()
    
def create_connection_nwk():
    conn = pyodbc.connect("DRIVER=Vertica;SERVER=dbgbivegap-nwk.corp.apple.com;DATABASE=GBIVEGAP;PORT=5433;UID=mystore_user;PWD=Find_me_usr#@nwk")
    return conn

def create_connection_redwood():
    conn = pyodbc.connect("DRIVER=Teradata;DBCNAME=redwood.corp.apple.com;UID=c1063159;PWD=Apple@1234;QUIETMODE=YES", autocommit=True,unicode_results=True)
    return conn

def close_connection(conn):
    conn.close()

def send_mail():
    body = open('test.html', 'rb').read()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Validation Result on ' + datetime.date.today().strftime('%B %d, %Y')
    HTML_BODY = MIMEText(body.encode('utf-8'), 'html','utf-8')
    msg.attach(HTML_BODY)
    s = smtplib.SMTP('relay.apple.com')
    s.sendmail('do_not_reply@apple.com', 'minat_verma@apple.com', msg.as_string())
    s.quit()

if __name__ == '__main__' :
    try :
        compare_data()
        send_mail()
    except :
        e = sys.exc_info()
        print e
