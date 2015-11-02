import json

def extract_json_end_time():
    path = r"/Users/Minat_Verma/Documents/My Tableau Repository/Logs/log.txt"
    with open(path,'rU') as file:
        for line in file:
            if 'end-query' in line:
                try:
                    query, time_taken = extract_sql_time(line)
                    writeFile(query, time_taken)
                except:
                    continue

def extract_sql_time(content_json):
    try:
        content_json = content_json.replace('\n','')
        content = json.loads(content_json)
        dict = content['v']
        query = dict['query']
        time_taken = dict['elapsed']
        return query,time_taken
    except ValueError:
        print "Value Error occurred "
    else :
        print "something is wrong in files.."

def writeFile(query, time_taken):
    with open("/Users/Minat_Verma/Documents/My Tableau Repository/tableau_log_queries_time.sql", 'a+') as file:
        file.seek(0)
        file.write('--time taken by below query '+ str(time_taken)+ ' seconds\n')
        file.write(query+';')
        file.write('\n\n')

if __name__ == '__main__':
    extract_json_end_time()
