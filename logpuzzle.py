#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

def read_urls(filename):
    host_name = 'http://'+filename.split('_')[1]
    urllist = []
    url=''
    with open(filename,'rU') as contents:
        for line in contents:
            object = re.search(r'(GET\s+)+(.+puzzle.+)+(\s+HTTP)',line)
            if object:
                url = object.group(2)
                if url not in urllist:
                    if url: # check for empty list
                        urllist.append(host_name+url)
    return sorted(urllist)


def download_images(img_urls, dest_dir):
    header = '''<verbatim>
            <html>
            <body>'''
    footer = '''</body>
            </html>'''
    image_string=''
    try:
        os.mkdir(dest_dir)
    except OSError:
        if os.path.exists(dest_dir):
            pass
        else:
            raise
    with open(dest_dir+'/index.html','w') as file:
        file.write(header)
        print 'Downloading...'
        for i,url in enumerate(img_urls):
            urllib.urlretrieve(url,dest_dir+'/img'+str(i))
            file.write('<img src="'+'img'+str(i)+'">')
        file.write(footer)
    file.close()


def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: [--todir dir] logfile '
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])
    for i,j in enumerate(img_urls):
        print i,j
        
    if todir:
        download_images(img_urls, todir)
    else:
        print '\n'.join(img_urls)

if __name__ == '__main__':
    main()
