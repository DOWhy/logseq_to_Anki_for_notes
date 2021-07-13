# -*- coding: utf-8 

import markdown
import os
import sys
import re
import time
import document_content_process
import markdown2html
import file_properties

if __name__ == "__main__":

    # anki = [] # 用来存放那些即将导入anki的 问答题
    anki = []

    path = 'C:\\Users\\john\\Videos\\Logseq\\logseq-obsidian-notes\\pages\\'  # 要处理的笔记目录

    questionPath = 'C:\\Users\\john\\Downloads\\question.txt'

    content = ''
    fileList = os.listdir(path)

    count = 0  # 用来计数，看看处理了多少个文件
    for file in fileList:

        count = count + 1
        # print(count)
        

        if file.endswith('.md'):

        # TODO 文件属性修改时间，只处理某个时间之后的文件
            mtime = os.path.getmtime(path + file)
            lastTimeOfToAnki = file_properties.getLastTimeOfToAnki()

            if mtime > lastTimeOfToAnki:

                file1 = open(path + file, encoding='utf-8')
                conlist = file1.readlines()
                file1.close()

                i = 0
                for i in range(len(conlist)):
                    if '#[[AnkiCard]]' in conlist[i]:
                        content = ''
                        if conlist[i].startswith('-'):
                            j = i+1
                            while conlist[j].startswith('\t'):
                                content = content + conlist[j][1:]
                                j = j+1
                        else:
                            k = 0
                            for k in range(len(conlist[i])):
                                if conlist[i][k] != '\t':
                                    tab_Number = k
                                    print(tab_Number)
                                    break
                            j = i+1
                            print('t'*(tab_Number+1))
                            while j < len(conlist) and conlist[j].startswith('\t'*(tab_Number+1)):
                                content = content + conlist[j][tab_Number+1:]
                                print(conlist[j][tab_Number+1:])
                                j = j+1

                        html = markdown.markdown(content, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
                        html = '@%@%' + html + '@%@%'
                        conlist[i] = conlist[i].replace('\t', '')
                        question = markdown.markdown(conlist[i][:-1], extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
                        question = '@%@%' + question + '@%@%'
                        id = re.search(r'(\d{14})', conlist[i]).group(1)
                        html = id + '\t' + question + '\t' + html + '\n'
                        anki.append(html)

    file2 = open(questionPath, 'w', encoding='utf-8')
    file2.writelines(anki)
    file2.close()


    file_properties.saveTheTimeOfToAnki(time.time())


    markdown2html.turnInlineLinkToRed(questionPath)
    markdown2html.turnDeleteLine(questionPath)
    markdown2html.turnInlineLatex(questionPath)
    markdown2html.copyMediaToAnki(questionPath)




    questionTxt = open(questionPath, encoding='utf-8')
    content = questionTxt.read()
    questionTxt.close()

    # 将 question.txt 中的双引号都变成成对的双引号
    # 将 question.txt 中的 @%@% 变成双引号  # 因为用引号标明字段，所以字段内的引号要用成对的。见：https://docs.ankiweb.net/importing.html
    content = content.replace('"', '""')
    content = content.replace('@%@%', '"')

    questionTxt = open(questionPath, 'w', encoding='utf-8')
    questionTxt.write(content)
    questionTxt.close()