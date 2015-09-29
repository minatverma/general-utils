import sys
import os
import string
import re

def open_file():
    path = raw_input( "\n\nEnter complete file path below:\n" ).strip(' ')
    file = open(path, 'rU')
    file_contents = file.read()
    file_contents = file_contents.replace('(', ' ( ')
    file_contents = file_contents.replace(')', ' ) ')
    file.close()
    return file_contents

def remove_quotes_comments(str):
    quote_list = re.findall(r'\'.+\'',str)
    for a in xrange(len(quote_list)):   
        str = str.replace(quote_list[a],' ')
    comment_list_1 = re.findall(r'--.+\n',str)
    for a in xrange(len(comment_list_1)):   
        str = str.replace(comment_list_1[a],' ')
    comment_list_2 = re.findall(r'//*.+/*/',str)
    for a in xrange(len(comment_list_2)):   
        str = str.replace(comment_list_2[a],' ')
    extract_list = re.findall(r'EXTRACT(.+)',str)
    for a in xrange(len(extract_list)):   
        str = str.replace(extract_list[a],' ')
    return str

def nextword(target, source):
    for i, w in enumerate(source):
        if w == target:
            return source[i+1]

def get_from_count(wordlist):
    count_from = 0
    for word in wordlist:
        if word == 'from':
            count_from = count_from + 1
    return count_from

def get_join_count(wordlist):
    count_join = 0
    for word in wordlist:
        if word == 'join':
            count_join = count_join + 1
    return count_join

def get_into_count(wordlist):
    into_count = 0
    for word in wordlist:
        if word == 'insert':
            into_count = into_count + 1
    return into_count

def get_all_objects(sql):
    from_object_list = []
    join_object_list = []
    into_object_list = []
    work_string = sql.split()
    from_count = get_from_count(work_string)
    join_count = get_join_count(work_string)
    into_count = get_into_count(work_string)
    try:
        into_object_list.append(nextword('into',re.search(r'insert\s+into\s+\w+\.\w+',sql).group().split()))
    except:
        pass
    try:
        into_object_list.append(nextword('into',re.search(r'merge\s+into\s+\w+\.\w+',sql).group().split()))
    except:
        pass
    for times in xrange(from_count):
        from_object_list.append(nextword('from',work_string))
        work_string = work_string[work_string.index(nextword('from',work_string)):]
    work_string = sql.split()
    for times in xrange(join_count):
        join_object_list.append(nextword('join',work_string))
        work_string = work_string[work_string.index(nextword('join',work_string)):]
    all_source_objects = from_object_list + join_object_list
    all_target_objects = into_object_list
    return all_source_objects, all_target_objects

def main():
    file = remove_quotes_comments(open_file()).lower()
    master_source_list = []
    master_target_list = []
    all_source_objects_cleaned = []
    all_target_objects_cleaned = []
    all_work_objects = []
    all_sqls = file.split(';')
    for sql in all_sqls:
        all_source_objects, all_target_objects = get_all_objects(sql)
        master_source_list = master_source_list + all_source_objects
        master_target_list = master_target_list + all_target_objects
    [all_source_objects_cleaned.append(x) for x in master_source_list if x not in all_source_objects_cleaned]    
    if ('(') in all_source_objects_cleaned:
        all_source_objects_cleaned.remove('(')
    [all_target_objects_cleaned.append(x) for x in master_target_list if x not in all_target_objects_cleaned]    
    if ('(') in all_target_objects_cleaned:
        all_target_objects_cleaned.remove('(')
    all_source_objects_cleaned = [item for item in all_source_objects_cleaned if item not in all_target_objects_cleaned]
    all_target_objects_cleaned = [item for item in all_target_objects_cleaned if item not in all_source_objects_cleaned]
    all_work_objects = [item for item in all_target_objects_cleaned if 'wrk' in item]
    all_target_objects_cleaned = [item for item in all_target_objects_cleaned if item not in all_work_objects]
    all_work_objects = all_work_objects + [item for item in all_source_objects_cleaned if 'wrk' in item]
    all_source_objects_cleaned = [item for item in all_source_objects_cleaned if item not in all_work_objects]
    print '\n\n\t Source Objects\n'+'_'*40+'\n'
    for index, item in enumerate(sorted(all_source_objects_cleaned)):
        print str(index+1)+'\t'+ item
    print '\n\n\t Target Objects\n'+'_'*40+'\n'
    for index, item in enumerate(sorted(all_target_objects_cleaned)):
        print str(index+1)+'\t'+ item
    print '\n\n\t Work Objects\n'+'_'*40+'\n'
    for index, item in enumerate(sorted(all_work_objects)):
        print str(index+1)+'\t'+ item
    print '\n\n\n'

if __name__ == '__main__':
    main()
