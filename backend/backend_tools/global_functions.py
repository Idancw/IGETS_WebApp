from subprocess import getoutput
from os import makedirs, remove, listdir
from os.path import dirname
import shutil


def check_report_state(path):
    if 'report.html' in listdir(path):
        return 'Yes'
    return 'No'


def report_state(path):
    if 'report.html' in listdir(path):
        with open('{}/report.html'.format(path), 'r') as f:
            if 'Pass' in f.readline():
                return 'Pass'
            return 'Unstable'
    return '---'


def report_link(path):
    if 'report.html' in listdir(path):
        return '{}/report.html'.format(path)
    return ''


def copy_files(images=[], src_path='', dst_path='', move=False):
    if src_path and dst_path:
        cmd = 'cp -r {} {}'.format(src_path, dst_path)
        if move:
            cmd = 'mv {} {}'.format(src_path, dst_path)
        getoutput(cmd)
    if images:
        for img in images:
            dst_path = '../frontend/{}'.format(dirname(img))
            try:
                makedirs(dst_path)
            except:
                pass
            cp_cmd = 'cp {} ../frontend/{}'.format(img.replace('static/', ''), img)
            getoutput(cp_cmd)


def remove_files(dir_path, remove_dir=False):
    # print('remove_files({}, {})'.format(dir_path, remove_dir))
    if remove_dir:
        # print('remove dir: ' + dir_path)
        shutil.rmtree(dir_path)
    else:
        # print('remove file: ')
        for _file in listdir(dir_path):
            # print('remove: ' + dir_path + _file)
            remove(dir_path + _file)

