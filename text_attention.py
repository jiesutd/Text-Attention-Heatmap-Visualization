# -*- coding: utf-8 -*-
# @Author: Jie Yang
# @Date:   2019-03-29 16:10:23
# @Last Modified by:   Jie Yang,     Contact: jieynlp@gmail.com
# @Last Modified time: 2019-04-12 09:56:12


## convert the text/attention list to latex code, which will further generates the text heatmap based on attention weights.
import numpy as np

latex_special_token = ["!@#$%^&*()"]

def generate(text_list, attention_list, latex_file, color='red', rescale_value = False):
	assert(len(text_list) == len(attention_list))
	if rescale_value:
		attention_list = rescale(attention_list)
	word_num = len(text_list)
	text_list = clean_word(text_list)
	with open(latex_file,'w') as f:
		f.write(r'''\documentclass[varwidth]{standalone}
\special{papersize=210mm,297mm}
\usepackage{color}
\usepackage{tcolorbox}
\usepackage{CJK}
\usepackage{adjustbox}
\tcbset{width=0.9\textwidth,boxrule=0pt,colback=red,arc=0pt,auto outer arc,left=0pt,right=0pt,boxsep=5pt}
\begin{document}
\begin{CJK*}{UTF8}{gbsn}'''+'\n')
		string = r'''{\setlength{\fboxsep}{0pt}\colorbox{white!0}{\parbox{0.9\textwidth}{'''+"\n"
		for idx in range(word_num):
			string += "\\colorbox{%s!%s}{"%(color, attention_list[idx])+"\\strut " + text_list[idx]+"} "
		string += "\n}}}"
		f.write(string+'\n')
		f.write(r'''\end{CJK*}
\end{document}''')

def rescale(input_list):
	the_array = np.asarray(input_list)
	the_max = np.max(the_array)
	the_min = np.min(the_array)
	rescale = (the_array - the_min)/(the_max-the_min)*100
	return rescale.tolist()


def clean_word(word_list):
	new_word_list = []
	for word in word_list:
		for latex_sensitive in ["\\", "%", "&", "^", "#", "_",  "{", "}"]:
			if latex_sensitive in word:
				word = word.replace(latex_sensitive, '\\'+latex_sensitive)
		new_word_list.append(word)
	return new_word_list


if __name__ == '__main__':
	## This is a demo:

	sent = '''the USS Ronald Reagan - an aircraft carrier docked in Japan - during his tour of the region, vowing to "defeat any attack and meet any use of conventional or nuclear weapons with an overwhelming and effective American response".
North Korea and the US have ratcheted up tensions in recent weeks and the movement of the strike group had raised the question of a pre-emptive strike by the US.
On Wednesday, Mr Pence described the country as the "most dangerous and urgent threat to peace and security" in the Asia-Pacific.'''
	sent = '''我 回忆 起 我 曾经 在 大学 年代 ， 我们 经常 喜欢 玩 “ Hawaii guitar ” 。 说起 Guitar ， 我 想起 了 西游记 里 的 琵琶精 。
	今年 下半年 ， 中 美 合拍 的 西游记 即将 正式 开机 ， 我 继续 扮演 美猴王 孙悟空 ， 我 会 用 美猴王 艺术 形象 努力 创造 一 个 正能量 的 形象 ， 文 体 两 开花 ， 弘扬 中华 文化 ， 希望 大家 能 多多 关注 。'''
	words = sent.split()
	word_num = len(words)
	attention = [(x+1.)/word_num*100 for x in range(word_num)]
	import random
	random.seed(42)
	random.shuffle(attention)
	color = 'red'
	generate(words, attention, "sample.tex", color)