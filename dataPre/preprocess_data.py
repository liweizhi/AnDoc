#coding=utf-8
#author: James Lee, THU

import os


class TABFILE:
    def __init__(self, filename, dest_file=None):
        self.filename = filename
        if not dest_file:
            self.dest_file = filename
        else:
            self.dest_file = dest_file
        self.filehandle = None
        self.content = []
        self.initflag = False
        self.Column = 0
        self.Row = 0
        self.data = []
        self.head = []

    def Init(self):
        try:
            self.filehandle = open(self.filename, 'r')
            self.initflag = self._load_file()
        except:
            pass
        else:
            self.initflag = True
        return self.initflag

    def UnInit(self):
        if self.initflag:
            self.filehandle.close()

    def _load_file(self):
        if self.filehandle:
            self.content = self.filehandle.readlines()
            self.Row = len(self.content)
            self.head = self.content[0].split('\t')
            self.Column = len(self.head)
            for line in self.content:
                # 这里需要去掉末尾的换行
                # line = line - '\n\r'
                self.data.append(line.rstrip().split('\t'))
            return True
        else:
            return False

    def GetValue(self, row, column):

        if 0 <= row < self.Row and 0 <= column < self.Column:
            return self.data[row][column]
        else:
            return None

    def SetValue(self, row, column, value):
        if 0 <= row < self.Row and 0 <= column < self.Column:
            self.data[row][column] = value
        else:
            return False

    def SaveToFile(self):
        filewrite = open(self.dest_file, 'w')
        if not filewrite:
            return False
        sep_char = '\t'
        for line in self.data:
            filewrite.write(sep_char.join(line) + '\n')
        filewrite.close()
        return True


def IterateFiles(directory):
    assert os.path.isdir(directory)
    result = []
    for root, dirs, files in os.walk(directory, topdown=True):
        for fl in files:
            result.append(os.path.join(root, fl))

    return result

#taskid fpackagename fapp_name ftargetwbg
def ProcessReuslt(result):
    dic = {}
    print 'result row: ', result.Row
    for i in range(1, result.Row):
        task_id = result.GetValue(i, 10)
        value = []
        value.append(result.GetValue(i, 10))
        value.append(result.GetValue(i, 17))
        value.append(result.GetValue(i, 19))
        if result.GetValue(i, 0) == 'Black':
            value.append(1)
        else:
            value.append(0)
        dic[task_id] = value;
    return dic


#taskid fpackagename fapp_name ftargetwbg fop fop fdata ftime
def ProcessLog(log, result_dic, log_dic):
    print 'log row: ', log.Row
    for i in range(1, log.Row):
        task_id = log.GetValue(i, 8)
        if task_id not in result_dic:
            continue
        if task_id not in log_dic:
            log_dic[task_id] = []
        value = []
        value.extend(result_dic[task_id])
        value.append(log.GetValue(i, 4)) #fop
        value.append(log.GetValue(i, 2)) #fdata
        value.append(log.GetValue(i, 5)) #ftime
        log_dic[task_id].append(value)
    return log_dic


def SaveData(log_dic, dir):
    for key, value in log_dic:
        filename = key + '.txt';
        filename = os.path.join(dir, filename)
        filewrite = open(filename, 'w')
        if not filewrite:
            return False
        sep_char = '\t'
        head = ['task_id', 'package_name', 'app_name', 'target', 'operation', 'op_data', 'time'];
        filewrite.write(sep_char.join(head) + '\n')
        for etem in value:
            filewrite.write(sep_char.join(etem) + '\n')
        filewrite.close()
        print 'save taskid file'
    return True


if __name__ == '__main__':

    result = TABFILE('/Users/james/tencent/data/tb_apk_detect_result_20170718.txt')
    result.Init()
    result_dic = ProcessReuslt(result)
    result.UnInit()
    dirlist = IterateFiles('/Users/james/tencent/data/tb_run_log2_20170718')
    print dirlist
    log_dic = {}
    for filepath in dirlist:
        log = TABFILE(filepath)
        log.Init()
        log_dic = ProcessLog(log, result_dic, log_dic)
        log.UnInit()
        print 'save log_dic of file :' + filepath
    SaveData(log_dic, '/Users/james/tencent/data/predata_20170718')





