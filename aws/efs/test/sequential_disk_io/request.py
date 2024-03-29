import subprocess
import time
from threading import Thread


def requester(bs, fs, test):
    subprocess.check_call(
        "\curl 'https://oma3z82y67.execute-api.ap-northeast-2.amazonaws.com/version1/efs-test/?bs=%22'{}'%22&fs=%22'{}'%22&test=%22'{}'%22&count=%22'{}'%22#'".format(
            bs, fs, test, '0'),
        shell=True)
    subprocess.check_call(
        "\curl 'https://oma3z82y67.execute-api.ap-northeast-2.amazonaws.com/version1/tmp-test/?bs=%22'{}'%22&fs=%22'{}'%22&test=%22'{}'%22&count=%22'{}'%22#'".format(
            bs, fs, test, '0'),
        shell=True)


# fs(MB) if fs = 1 -> 1MB
test_set1 = [
    {'bs': '1', 'fs': '10', 'test': 'test1'},
    {'bs': '50', 'fs': '10', 'test': 'test1'},
    {'bs': '512', 'fs': '10', 'test': 'test1'},
    {'bs': '1024', 'fs': '10', 'test': 'test1'},
    {'bs': '2048', 'fs': '10', 'test': 'test1'},
]
# testing bs changes
test_set2 = [
    {'bs': '1024', 'fs': '1', 'test': 'test2'},
    {'bs': '1024', 'fs': '2', 'test': 'test2'},
    {'bs': '1024', 'fs': '3', 'test': 'test2'},
    {'bs': '1024', 'fs': '4', 'test': 'test2'},
    {'bs': '1024', 'fs': '5', 'test': 'test2'},
    {'bs': '1024', 'fs': '6', 'test': 'test2'},
]
# testing cold start using efs
test_set3 = [
    {'bs': '512', 'fs': '1', 'test': 'test3'},
    {'bs': '512', 'fs': '1', 'test': 'test3'},
    {'bs': '1024', 'fs': '5', 'test': 'test3'},
    {'bs': '1024', 'fs': '5', 'test': 'test3'},
]

threads_1 = []
for obj in test_set1:
    t = Thread(target=requester, args=(obj['bs'], obj['fs'], obj['test']))
    t.start()
    threads_1.append(t)
for t in threads_1:
    t.join()
# for obj in test_set1:
#     requester(obj['bs'], obj['fs'], obj['test'])
#
# for obj in test_set2:
#     requester(obj['bs'], obj['fs'], obj['test'])
#
# for obj in test_set3:
#     requester(obj['bs'], obj['fs'], obj['test'])
