import os, shutil
def new_report(test_report, dst):
    lists = os.listdir(test_report)                                    #列出目录的下所有文件和文件夹保存到lists
    #print(list)
    lists.sort(key=lambda fn:os.path.getmtime(test_report + "\\" + fn))#按时间排序
    #print(lists)
    listLength = len(lists)
    flag = False
    #print(test_report+lists[0])
    if (listLength == 1):
        file_new = os.path.join(test_report,lists[-1])                     #获取最新的文件保存到file_new
        flag = False
        return flag, file_new
    else:
        file_new = os.path.join(test_report, lists[-1])
        for i in range(listLength-1):
            shutil.move(test_report+"/"+lists[i], dst)
        flag = True
        return flag, file_new
if __name__=="__main__":
    test_report="C:\ca_project\Demo/front"#目录地址
    flag, filename = new_report('C:/ca_project/Demo/front', 'C:/ca_project/Demo/frontfinal')
    print(flag, filename)