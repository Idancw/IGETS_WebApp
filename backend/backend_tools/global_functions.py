from os import listdir


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

