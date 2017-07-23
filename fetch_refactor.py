#-*- coding:utf-8 -*-
#--author = 'wangyan'
import re
import subprocess
import os
import platform
addr_rep = ['https://github.com/ZTEwangyan/rep1.git','https://github.com/ZTEwangyan/rep2.git','https://github.com/ZTEwangyan/rep3.git']
dest_rep = ['E:\UTAC\\rep1','E:\LTE\\rep2',"E:\LTE\\rep3"]
rep_dict = {}
SEPA_PATT = re.compile(r'\\')
FORMAT = '--pretty=format: %h %an %ad  %s'
# create a dict to store the reposition and the branches
def init():
    plat = platform.platform()
    if 'Linux' in plat:
        SEPA_PATT = re.compile(r'/')
def last_of_path(patt,repo_str):
    #pattern = re.compile(r'\\')
    res      = re.split(patt,repo_str)
    return res[len(res)-1]
'''def last_of_path2(repo_str):
    pattern = re.compile(r'/')
    res     = re.split(pattern,repo_str)
    return res[len(res)-1]'''
def fetch_all_branches(repo,index):
    # get the master branch:
    branches = []
    cmd_master = ['git', 'clone', addr_rep[index], dest_rep[index]]
    subprocess.check_output(cmd_master,shell=True)
    # get the other branches:
    # print('subprocess exec sucessfully')
    os.chdir(dest_rep[index])
    cmd_slave = ['git', 'branch', '-a']
    stdout = subprocess.check_output(cmd_slave,shell=True)
    for each in stdout.splitlines():
        if re.match('\*.',each,re.IGNORECASE):
            master = each[2:]
        elif (not re.match('.*master', each, re.IGNORECASE)):
            branches.append(last_of_path(re.compile(r'/'),each))
    for branch in branches:
        command_new_branch = ['git','checkout','-b',branch,'origin/'+branch]
        subprocess.check_output(command_new_branch,shell=True)
    branches.append(master)
    # save the branches in repository
    rep_dict.update({repo:branches})
def fetch():
    for index in range(0,len(dest_rep)):
        repo_name = last_of_path(SEPA_PATT,dest_rep[index])
        fetch_all_branches(repo_name,index)
def getlog():
    while(True):
        print('total '+str(len(dest_rep))+' repositions: '+str(rep_dict.keys()))
        rep_in = raw_input('please select one,enter q to quit \n')
        if(rep_in == 'q'):
            break
        if rep_in in rep_dict.keys():
            for each in dest_rep:
                if rep_in in each:
                    os.chdir(each)
            print('branches in rep_in are:' + str(rep_dict.get(rep_in)))
            branch = raw_input('which branch\'s log do you want?\n')
            if branch in rep_dict.get(rep_in):
                check_cmd = ['git','checkout',branch]
                subprocess.check_output(check_cmd,shell=True)
                cmd = ['git','log',FORMAT]
                stdout = subprocess.check_output(cmd,shell=True)
                print(stdout)
if __name__ == '__main__':
    init()
    fetch()
    getlog()