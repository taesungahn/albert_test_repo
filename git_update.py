#-*- coding:utf-8 -*-
#!/usr/bin/env python
# by Albert
# PromptInsight local version과 remote version 비교 후 업데이트 (github에서 업데이트 데이터 받기)
# 패치서버: git 사용해 간단하게 구현
import os
import re

class GitUpdate():
    def __init__(self):
        self.patterns = {
            'engine':'\+engine,([0-9]+)$',
            'prompt':'\+prompt,([0-9]+)$',
            'plugin':'\+plugin,([0-9]+)$'
        }
        self.l_engine = None # local engine version
        self.r_engine = None # remote engine version
        self.l_prompt = None # local prompt version
        self.r_prompt = None # remote engine version
        self.l_plugin = None # local plugin version
        self.r_plugin = None # remote plugin version
        
    def __getVersions(self, file_name, diff):
        engine_v = prompt_v = plugin_v = None 
        with open(file_name, 'r', encoding='utf-8') as diff_file:
            lines = diff_file.readlines()
            for line in lines:
                line = line.strip()
                line = line.lower()
                line = line.replace(' ','')
                if diff==False: line = '+{}'.format(line)        
                if len(line) > 0:
                    for key_, pattern_ in self.patterns.items():
                        m = re.findall(pattern_, line)
                        if len(m) > 0:
                            if key_ == 'engine': 
                                if diff: self.r_engine = ''.join(m)
                                else: self.l_engine = ''.join(m)
                            elif key_ == 'prompt': 
                                if diff: self.r_prompt = ''.join(m)
                                else: self.l_prompt = ''.join(m)
                            elif key_ == 'plugin': 
                                if diff: self.r_plugin = ''.join(m)
                                else: self.l_plugin = ''.join(m)


    def local_check(self):
        return self.__getVersions('patch.txt', diff=False)

    def remote_check(self):
        os.system("git fetch")
        os.system("git diff main origin/main patch.txt > git_diff.txt")
        self.__getVersions('git_diff.txt', diff=True)
        if self.r_engine == None: 
            self.r_engine = self.l_engine
        if self.r_prompt == None:
            self.r_prompt = self.l_prompt
        if self.r_plugin == None:
            self.r_plugin = self.l_plugin

    def check_update(self):
        self.local_check()
        self.remote_check()      
        return {'local':{'engine':self.l_engine, 'prompt':self.l_prompt, 'plugin':self.l_plugin}, 
                'remote':{'engine':self.r_engine, 'prompt':self.r_prompt, 'plugin':self.r_plugin}}

    def update(self):
        os.system("git pull")

if __name__ == "__main__":
    gitUpdate = GitUpdate()
    ret = gitUpdate.check_update()