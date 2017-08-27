#!/usr/bin/python
# coding:utf-8
"""
    comments here
"""
__author__ = 'rmk'
import os
import cPickle as pkl


def preprocess(log_dir, resultfile_path):
    result_dict = {}
    log_dict = {}
    op_set = set()
    with open(resultfile_path) as f:
        # ftargetwbg^Iffilepath^Iftime^Iforiginmd5^Ifsubmd5^Ifmsg^Ifruleid^Iftype^Ifmd5^Ifsrcid^Iftaskid^Iftargetvirus^Ifcurwbg^Ifcurvirus^Ifarea^Iftargetsolution^Ifcursolution^Ifpackagename^Ifssdeep^Ifapp_name$

        for line in f.readlines()[1:]:
            line = line.split("\t")
            if len(line) != 20:
                print("Malformed line %s" % ("\t".join(line)))
                continue
            line = [l.strip() for l in line]
            label = line[0]  # Black 或者空
            time = line[2]
            taskid = line[10]
            packagename=line[17]
            appname = line[19]
            result_dict[taskid] = ["1" if label=="Black" else "0", time, taskid, packagename, appname]
            log_dict[taskid] = []
    print 'result_dic size:', len(result_dict)
    for logfile in os.listdir(log_dir):
        if not logfile.endswith(".txt"):
            continue
        print("processing %s" % os.path.join(log_dir, logfile))
        with open(os.path.join(log_dir, logfile)) as f:
            for line in f.readlines()[1:]:
                line = line.split("\t")

                if len(line) != 9:
                    print("Malformed line %s" % ("\t".join(line)))
                    continue
                line = [l.strip() for l in line]
                fdata=line[2]
                fop = line[4]
                ftaskid=line[8]
                if ftaskid not in result_dict:
                    # print("Skipping taskid %s " % (ftaskid))
                    continue
                else:
                    log_dict[ftaskid].append([fop, fdata])
                    op_set.add(fop)
    prefix = "./preprocessed"
    feature_dict = {}
    print("OP Size %d" % (len(op_set)))
    with open(os.path.join(prefix, "dict.txt"), "w") as dictfw:
        for i, op in enumerate(op_set):
            dictfw.write(op + "\t" + str(i))
            feature_dict[i] = op

    print("Writing to result file.")
    outx = []
    outy=[]
    for k, v in result_dict.items():
        if k not in log_dict:
            print("Result taskid %s not in log, skipping..." % (k))
            continue
        feature_array=[0]*len(feature_dict)
        for l in log_dict[k]:
            feature_array[feature_dict[l]] = 1

        outx.append(feature_array)
        outy.append(v[0])
    print "Writing to file"
    with open("./pre.pkl", "w") as fpre:
        pkl.dump([outx, outy], fpre)


    # 写入到文件

    # print("Writing to result file.")
    # with open(os.path.join(prefix,"result.txt"), "w") as fw:
    #     for k, v in result_dict.items():
    #         if k not in log_dict:
    #             print("Result taskid %s not in log, skipping..." % (k))
    #             continue
    #         fw.write("\t".join(v)+"\n")
    #         with open(os.path.join(prefix, k), "w") as logfw:
    #             print("writing ops for taskid %s, line conut %d" % (k, len(log_dict)))
    #             for l in log_dict[k]:
    #                 print("Writing %s " % "\t".join(l))
    #                 logfw.write("\t".join(l)+"\n")










    pass

if __name__ == "__main__":
    # TODO: do something here
    preprocess(log_dir="/Users/james/tencent/data/tb_run_log2_20170718",
               resultfile_path="/Users/james/tencent/data/tb_apk_detect_result_20170718.txt")
    pass