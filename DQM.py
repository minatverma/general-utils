import os
import sys
import pandas as pd
import pyodbc
import sqlparse
from pandas.util.testing import assert_frame_equal
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
pyodbc.pooling = False

def dqm_newark() :
    conn_nwk = create_connection_nwk()
    dataframes_newark = []
    tgtfile = open('tgtqueries.sql', 'rU').read()
    querylist = tgtfile.split(';')
    querylist.pop()
    for query in querylist :
        dataframes_newark.append(pd.read_sql(query, conn_nwk))
    close_connection(conn_nwk)
    return dataframes_newark,querylist

def dqm_redwood() :
    conn_rw = create_connection_redwood()
    dataframes_redwood = []
    srcfile = open('srcqueries.sql', 'rU').read()
    querylist = srcfile.split(';')
    querylist.pop()
    for query in querylist :
        dataframes_redwood.append(pd.read_sql(query, conn_rw))
    close_connection(conn_rw)
    return dataframes_redwood,querylist

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
                background-color: #e3f0fa;
                color: #333;
                font-weight: 400;
                font-size: 14px;
            }
            .df tbody td,.df tbody th {
                color: #333;
                font-weight: 400;
                font-size: 12px;
            }
            .df tr:nth-child(even) {background: #f5fbff}
            .df tr:nth-child(odd) {background: #eaeaea}

            .df thead th:nth-child(1),.df tbody th:nth-child(1){
              width:10%;
            }
            
            .df th:nth-child(2),.df th:nth-child(3),
            .df td:nth-child(2),.df td:nth-child(3){
              width:22%;
            }
        </style>
    </head>
    <body>
    '''
    FOOTER = '''
    </body>
    </html>
    '''
    html_out = open('test.html', 'w')
    print "Cross DB validation Starts :"
    src_dataframes,querylist_redwood = dqm_redwood()
    tgt_dataframes,querylist_newark = dqm_newark()
    html_out.write(HEADER)
    for i in xrange(len(src_dataframes)):
        try:
          assert_frame_equal(src_dataframes[i], tgt_dataframes[i],check_names=False)
          color = '#DBFEDB'
          html_out.write('<p style="font: 12px consolas, sans-serif;background-color:'+color+';border-style:solid;border-color:yellow;border-width:0.5px;white-space: pre">'+'<br>Teradata Query<br>'+sqlparse.format(querylist_redwood[i], reindent=True,indent_width = 4, keyword_case='upper', identifier_case = 'lower')+'</p>')
          html_out.write(src_dataframes[i].to_html(classes='df'))
          html_out.write('<p style="font: 12px consolas, sans-serif;background-color:'+color+';border-style:solid;border-color:yellow;border-width:0.5px;white-space: pre">'+'<br>Vertica Query<br>'+sqlparse.format(querylist_newark[i], reindent=True,indent_width = 4, keyword_case='upper', identifier_case = 'lower')+'</p>')
          html_out.write(tgt_dataframes[i].to_html(classes='df'))
          print 'Data Matches'
        except :
          print sys.exc_info()
          color = '#FFEBEB'
          html_out.write('<p style="font: 12px consolas, sans-serif;background-color:'+color+';border-style:solid;border-color:yellow;border-width:0.5px;white-space: pre">'+'<br>Teradata Query<br>'+sqlparse.format(querylist_redwood[i], reindent=True,indent_width = 4, keyword_case='upper', identifier_case = 'lower')+'</p>')
          html_out.write(src_dataframes[i].to_html(classes='df'))
          html_out.write('<p style="font: 12px consolas, sans-serif;background-color:'+color+';border-style:solid;border-color:yellow;border-width:0.5px;white-space: pre">'+'<br>Vertica Query<br>'+sqlparse.format(querylist_newark[i], reindent=True,indent_width = 4, keyword_case='upper', identifier_case = 'lower')+'</p>')
          html_out.write(tgt_dataframes[i].to_html(classes='df'))
          continue
        finally:
            html_out.write(FOOTER)
            send_mail()
      
 
def create_connection_nwk():
    conn = pyodbc.connect("DRIVER=Vertica;SERVER=dbgbivegap-nwk.corp.apple.com;DATABASE=GBIVEGAP;PORT=5433;UID=mystore_user;PWD=Find_me_usr#@nwk")
    return conn

def create_connection_redwood():
    conn = pyodbc.connect("DRIVER=Teradata;DBCNAME=redwood.corp.apple.com;UID=c1063159;PWD=Apple@1234;QUIETMODE=YES", autocommit=True,unicode_results=True)
    return conn

def close_connection(conn):
    conn.close()

def send_mail():
    file = open('test.html', 'rU')
    body = file.read()
    file.close()
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
    except :
        e = sys.exc_info()
        print e
