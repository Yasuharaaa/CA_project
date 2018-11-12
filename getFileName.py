import os
def new_report(test_report):
    lists = os.listdir(test_report)                                    #列出目录的下所有文件和文件夹保存到lists
    print(list)
    lists.sort(key=lambda fn:os.path.getmtime(test_report + "\\" + fn))#按时间排序
    file_new = os.path.join(test_report,lists[-1])                     #获取最新的文件保存到file_new
    #print(file_new)
    return file_new
if __name__=="__main__":
    test_report="C:\PyTorch\hymenoptera_data/train/ants"#目录地址
    new_report(test_report)