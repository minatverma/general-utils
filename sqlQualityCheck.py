#Embedded file name: sql_quality_check.py
"""sql_quality_check.py accepts a file name and runs code quality
analysis on it. 
"""
import os
import sys
import re

def CheckKeyword(word):
    KEYWORD_LIST = ('ALL', 'ABS', 'ACCESS', 'ACTIVITY_COUNT', 'ADD_MONTHS', 'AFTER', 'ALTER', 'AND', 'ANY', 'AS', 'AT', 'AVE', 'AVERAGE', 'BEGIN', 'BEFORE', 'BETWEEN', 'BIGINT', 'BINARY', 'BT', 'BUT', 'BY', 'BYTEINT', 'BYTE', 'CALL', 'CASE', 'CASESPECIFIC', 'CAST', 'CHAR', 'CHARACTER', 'CHECKPOINT', 'COALESCE', 'COLLECT', 'COLUMN', 'CLOB', 'COMMIT', 'COMPRESS', 'COUNT', 'CREATE', 'CSUM', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURSOR', 'DATABASE', 'DATE', 'DAY', 'DECIMAL', 'DECLARE', 'DEFAULT', 'DELETE', 'DEL', 'DISTINCT', 'DO', 'DOUBLE', 'DROP', 'EACH', 'ELSE', 'ELSEIF', 'ERROR', 'ERRORTABLES', 'ESCAPE', 'END', 'ET', 'EXECUTE', 'EXCEPT', 'EXIT', 'EXTRACT', 'FETCH', 'FIRST', 'FOR', 'FROM', 'FULL', 'GROUP', 'HANDLER', 'HAVING', 'HELP', 'HOUR', 'IDENTITY', 'IF', 'IMMEDIATE', 'IN', 'INOUT', 'INNER', 'INSERT', 'INTEGER', 'INTERSECT', 'INTO', 'INTERVAL', 'IS', 'ITERATEAR', 'JOIN', 'JOURNAL', 'LE', 'LEADING', 'LEFT', 'LIKE', 'LOCKING', 'LOGGING', 'LOOP', 'LOWER', 'LT', 'MATCHED', 'MINIMUM', 'MAX', 'MERGE', 'MIN', 'MINUS', 'MINUTE', 'MONTH', 'NOT', 'NON', 'NO', 'NULLAR', 'NULLIF', 'NULL', 'NUMBER', 'NUMERIC', 'ON', 'OR', 'ORDER', 'OUT', 'OUTER', 'PROCEDURE', 'RANDOM', 'REPLACE', 'RETURN', 'RIGHT', 'ROLLBACK', 'ROW', 'ROW_NUMBER', 'SAMPLE', 'SECOND', 'SEL', 'SELECT', 'SESSION', 'SET', 'SMALLINT', 'SPOOL', 'SQLCODE', 'SQLEXCEPTION', 'SQLSTATE', 'SQLSTATE', 'STATISTICS', 'SUM', 'TABLE', 'THEN', 'TIMESTAMP', 'TO', 'TRIM', 'UNION', 'UPDATE', 'UPPER', 'USING', 'VARCHAR', 'VALUE', 'VALUES', 'VIEW', 'WHEN', 'WHERE', 'WHILE', 'WITH', 'YEAR')
    if str.upper(word) in KEYWORD_LIST:
        return True
    else:
        return False


def ValidateFile(file_name, log_file):
    line_no = 0
    case_count = 0
    code_score = 0
    case_count_moderate = 0
    prev_line_start = 1
    curr_line_start = 0
    line_empty = False
    multi_line_check = False
    positional_check = False
    quote_multi_line_check = False
    log_file.write('Starting logging for file \n' + file_name)
    for line in open(file_name):
        line_no += 1
        line, multi_line_check = RemoveCommentedText(line, multi_line_check)
        line, quote_multi_line_check = RemoveQuotedText(line, quote_multi_line_check)
        if len(line) > 0:
            curr_line_start = line.find(line.strip()) + 1
            if abs(curr_line_start - prev_line_start) not in (0, 4):
                log_file.write('Please check indentation for line  %5d ' % line_no + '\n')
                case_count_moderate += 1
            case_count += ValidateWord(line, line_no, log_file)
            prev_line_start = curr_line_start
        CheckPositionalCall(line, line_no, positional_check)

    print '\nEnd of file: ' + file_name
    code_score = 10 - case_count * 10 / line_no
    print 'Score : %4d' % code_score + ' Expected score: Above 9 ' + ' High Case count: %4d ' % case_count + 'Moderate case count %4d' % case_count_moderate


def ValidateWord(line, line_no, log_file):
    prob_case_count = 0
    for word1 in line.split():
        for word in re.sub('[:();=,]', ' ', word1).split():
            answer = CheckKeyword(word)
            if answer and str.upper(word) != word:
                log_file.write("  Keyword found : '" + word + "' Line %4d" % line_no + ' Not in upper case \n')
                prob_case_count += 1
            elif not answer and str.lower(word) != word and word[0] != "'" and word[-1] != "'":
                log_file.write("Improper case for : '" + word + "' Line %4d" % line_no + '\n')
                prob_case_count += 1

    return prob_case_count


def RemoveCommentedText(line, multi_line_check):
    temp_line = ''
    if multi_line_check:
        if line.find('*/') > 0:
            line = line[line.find('*/') + 2:]
            multi_line_check = False
        else:
            line = ''
    while line.count('/*') > 0:
        temp_line = temp_line + ' ' + line[0:line.find('/*')]
        if line.find('*/') > 0:
            line = temp_line + ' ' + line[line.find('*/') + 2:]
        else:
            line = temp_line
            multi_line_check = True

    line = line[0:str.find(str.strip(line), '--', 0)]
    return (line, multi_line_check)


def RemoveQuotedText(line, quote_multi_line_check):
    """ Removes all quoted phrases"""
    temp_line = ''
    if quote_multi_line_check:
        if line.find("'") > 0:
            line = line[line.find("'") + 1:]
            quote_multi_line_check = False
        else:
            line = ''
    while line.count("'") > 0:
        temp_line = (temp_line + ' ').lstrip() + line[0:line.find("'")]
        line = line[line.find("'") + 1:]
        if line.find("'") > 0:
            line = temp_line + ' ' + line[line.find("'") + 1:]
        else:
            line = temp_line
            quote_multi_line_check = True

    return (line, quote_multi_line_check)


def CheckPositionalCall(line, line_no, positional_check):
    if not positional_check and line.find('GROUP BY') > 0:
        positional_check = True
        line = line[line.find('GROUP BY') + 8:]
    if positional_check and is_number(line.strip()[0:1]):
        print 'CRITICAL ERROR: Positional parameter used in line %5d' % line_no
    if not positional_check and line.find('ORDER BY') > 0:
        positional_check = True
        line = line[line.find('ORDER BY') + 8:]
    if positional_check and is_number(line.strip()[0:1]):
        print 'CRITICAL ERROR: Positional parameter used in line %5d' % line_no


def is_number(string):
    """ Custom function to check if a string is numeric or not """
    try:
        float(string)
        return True
    except ValueError:
        return False


def TotalDeep(found_d, dir_name, files):
    """Checks for files with .spl extension and calls ValidateFile function."""
    global log_file_name
    for file in files:
        pname = dir_name + os.sep + file
        if not os.path.isfile(pname):
            continue
        try:
            if file.endswith('.spl'):
                print pname
                log_file_name = pname + '_log'
                log_file = open(log_file_name, 'w')
                ValidateFile(pname, log_file)
                log_file.close()
        except IOError as msg:
            print pname, msg


def main():
    while True:
        try:
            print 'Please enter starting directory'
            dir_name = raw_input('Directory path: ')
            break
        except (KeyboardInterrupt, EOFError):
            print
            break

        if file_name == '':
            break

    files_d = {}
    os.path.walk(dir_name, TotalDeep, files_d)


if __name__ == '__main__':
    main()
