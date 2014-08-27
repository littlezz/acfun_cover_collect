__author__ = 'zz'

import threading
import requests
from urllib import parse
import os
import queue
import pickle

import logging
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
_PHP_URL = "http://avdot.net/cover.php"



def mk_dir(parentpath, name):
    path = os.path.join(parentpath, name)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    return path

class DownloadedImage:

    #if continuous_exigist > 15, there is no more image should be download
    _exit_bound = 15

    def __init__(self):
        self._lock = threading.Lock()
        self._set = set()
        self.continuous_exigst = 0
    def exigst(self, key):
        with self._lock:
            if key in self._set:
                self.continuous_exigst += 1
                return True
            else:
                self.continuous_exigst = 0
                return False

    def add(self, key):
        with self._lock:
            self._set.add(key)

    def is_need_exit(self):
        return True if self.continuous_exigst > self._exit_bound else False

log_list=[]

def get_correct_url_and_filename():

    encoder = 'gbk'

    req = requests.head(_PHP_URL)
    parsed_url = parse.urlparse(req.headers['location'])
    logging.debug('error path is %s:',parsed_url.path)

    try:
        fix_path = parsed_url.path.encode('latin1').decode('gbk')
    except UnicodeDecodeError:
        fix_path = parsed_url.path.encode('latin1').decode('utf8')
        encoder = 'utf8'

    filename = fix_path.split('/')[-1]
    correct_path = parse.quote(fix_path,encoding=encoder)
    correct_url = parse.urlunsplit((parsed_url.scheme, parsed_url.netloc, correct_path, '', ''))


    return correct_url, filename



class Base:
    folder = 'images'

    def __init__(self):

        self.downloaded_set = DownloadedImage()

    def download(self, s):
        with s:
            url, filename = get_correct_url_and_filename()
            if self.downloaded_set.exigst(url):
                return
            else:
                print('download:',url)
                self.downloaded_set.add(url)
                content = requests.get(url).content
                with open(filename, 'wb') as f:
                    f.write(content)

    def is_finish(self):
        return self.downloaded_set.is_need_exit()


def main():
    mk_dir(os.getcwd(), Base.folder)
    os.chdir(Base.folder)
    base = Base()
    s = threading.Semaphore(3)
    target_list=queue.deque(maxlen=6)
    while True:
        for i in range(5):
            t = threading.Thread(target=base.download, args=(s,))
            t.start()
            target_list.append(t)

        for t in target_list:
            t.join()
        if base.is_finish():
            break

    while True:
        if  not any( t.is_alive() for t in target_list):
            break

if __name__ == '__main__':
    main()

