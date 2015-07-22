__author__ = 'zz'
import time
import threading
import requests
from urllib import parse
import os
import queue
import unicodedata
from fix_headers_parse import make_headers_fix
import logging

logging.basicConfig(level=logging.WARNING, format='%(threadName)s %(message)s')


_PHP_URL = "http://cover.acfunwiki.org/cover.php"
log_list = []


quit_thread = object()
make_headers_fix()


def safe_pathname(path):
    extra = '-_.'
    s = []

    for c in unicodedata.normalize('NFKC', path):
        cat = unicodedata.category(c)[0]
        if cat in 'LN' or c in extra:
            s.append(c)
        elif cat == 'Z':
            s.append(' ')

    return ''.join(s).strip()


def mk_dir(parentpath, name):
    path = os.path.join(parentpath, name)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    return path


class DownloadedImage:
    # if continuous_exigist > 55, there is no more image should be download
    _exit_bound = 55

    def __init__(self):
        self._lock = threading.Lock()
        self._set = set()
        self.continuous_exist = 0

    def exist(self, key):
        with self._lock:
            if key in self._set:
                self.continuous_exist += 1
                return True
            else:
                self.continuous_exist = 0
                return False

    def add(self, key):
        with self._lock:
            self._set.add(key)

    def is_need_exit(self):
        return self.continuous_exist > self._exit_bound

    def get_items_num(self):
        return len(self._set)


def get_url_and_filename():
    req = requests.head(_PHP_URL)
    url = req.headers['location']

    logging.warning('error path is %s:', url)

    path = parse.urlparse(url).path
    filename = safe_pathname(path.rsplit('/')[-1])

    return url, filename


class Base:
    folder = 'images'

    def __init__(self):
        self.downloaded_set = DownloadedImage()

    def download(self):

        url, filename = get_url_and_filename()
        if self.downloaded_set.exist(url):
            return
        else:
            self.downloaded_set.add(url)

            if os.path.exists(filename):
                return

            print('download:', url)
            res = requests.get(url)

            # I really do not know how fix the url path, fuuuuuuuuck
            if not res.ok:
                print('not ok', res.url, '\nraw', res.url.encode().decode('latin1'))

                return

            content = res.content
            with open(filename, 'wb') as f:
                f.write(content)

    def is_finish(self):
        return self.downloaded_set.is_need_exit()


class AcCoverDownloader(Base):

    def __init__(self, max_thread=8):
        self.max_thread = max_thread
        self._exit_thread_q = queue.Queue()
        super().__init__()

    def download(self):
        while not self.is_finish():
            super().download()

        self._exit_thread_q.put(quit_thread)

    def all_thread_quit(self):
        return self.max_thread == self._exit_thread_q.qsize()

    def start(self):
        for t in range(self.max_thread):
            threading.Thread(target=self.download).start()

        while not self.all_thread_quit():
            time.sleep(2)

        self.finish()

    def finish(self):
        print('Finish, download {} images'.format(self.downloaded_set.get_items_num()))


def main():
    mk_dir(os.getcwd(), Base.folder)
    os.chdir(Base.folder)

    acd = AcCoverDownloader()
    acd.start()


if __name__ == '__main__':
    main()
