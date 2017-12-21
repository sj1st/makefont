#!D:/green/ff171019_3/bin/ffpython.exe
# -*- coding: UTF-8 -*-
#"D:/green/ff171019_3/bin/fontforge" -script uu.py a.ttf
#将只有主unicode的字体补上从unicode
import os,fontforge,sys,codecs;

def charToUnicode(char):
	char_b = char.encode('utf-32be');
	return (((char_b[0] * 0x100 + char_b[1])* 0x100 + char_b[2])* 0x100 + char_b[3]);

def strSetStr(str):#字符串去重复
	l1 = list(str);
	l2 = [];
	for i in l1:
			if not i in l2:
				l2.append(i);
	return ''.join(l2);

def strSetStrDel(str,strd):#字符串去重复，并去掉指定字符
	l1 = list(str);
	l2 = [];
	for i in l1:
			if (not i in l2) and i != strd:
				l2.append(i);
	return ''.join(l2);


import charSis,charDau,charMe;
kanji_0 = charSis.kanji;
kanji_1 = charMe.kanji;
kanji_123 = charDau.kanji;

#统字：一对多的单个汉字。
kanji_11 = [];#统字表

#一对多汉字，首个汉字
for hanzis in kanji_123:
	if not hanzis[0] in kanji_11:
		kanji_11.append(hanzis[0]);

#一对多的 统合统字表
kanji_123_k =[];

for kanji in kanji_11:
	kanjis = '';#临时存放"分字"
	for hanzis in kanji_123:
		if kanji in hanzis:
			kanjis += hanzis;
	for hanzis in kanji_0:
		if kanji in hanzis:
			kanjis += hanzis;
	kanji_123_k.append(kanji+strSetStrDel(kanjis,kanji));



kanji_0_0 =[];#去除统字的 相同字表
kanji_0_y = kanji_0[:];#原来的同字表
while len(kanji_0) > 0:
	restart = False;#标记A
	hanzis = kanji_0.pop();#移除认最后一个元素，并且返回该元素的值。
	for kanji in hanzis:
		if kanji in kanji_11:
			restart = True;
			break;
	if restart:
		continue;
	kanji_0_0.append(hanzis);

#统合同字表
kanji_0_k =[];
#合并同字条
kanji_0_k.append(kanji_0_0.pop());
while len(kanji_0_0) > 0:
	hanzis = kanji_0_0.pop();
	restart = False;#标记A
	for kanji in hanzis:#同字条总的汉字
		for i in range(len(kanji_0_k)):
			if kanji in kanji_0_k[i]:
				restart = True;#标记A
				kanji_0_k[i] = strSetStr(kanji_0_k[i]+hanzis);
				break;
		if restart:
			break;
	if not restart:
		kanji_0_k.append(hanzis);

#file_object = codecs.open('a04.txt', 'w',"utf-8") ;
#for hanzis in kanji_123_k:
#		file_object.write("'"+hanzis+"',");
#		file_object.write("\r\n");
#file_object.close();

fontfile = sys.argv[1];
font = fontforge.open(fontfile);

for kanjis in kanji_0_k:#宽
	aa = '';#主
	bb = '';#副
	cc = '';#从
	for kanji in kanjis:
		kanji_unicode = charToUnicode(kanji);
		if not kanji_unicode in font:
			cc += kanji;
		else:
			if aa == '':
				if font[kanji_unicode].unicode == kanji_unicode:
					aa = kanji;
				else:
					if bb == '':
						bb = kanji;
	if  cc != '' and (aa != '' or bb != ''):
		if aa != '':
			font_kanji = aa;
		else:
			font_kanji = bb;
		altuni = font[charToUnicode(font_kanji)].altuni;
		for kanji in cc:
			if altuni == None:
				altuni = ((charToUnicode(kanji),-1,0),);
			else:
				altuni = altuni +((charToUnicode(kanji),-1,0),);
		font[charToUnicode(font_kanji)].altuni = altuni;

for kanjis in kanji_0_y:#严
	aa = '';#主
	cc = '';#从
	for kanji in kanjis:
		kanji_unicode = charToUnicode(kanji);
		if not kanji_unicode in font:
			cc += kanji;
		else:
			if aa == '':
				if font[kanji_unicode].unicode == kanji_unicode:
					aa = kanji;
	if  cc != '' and aa != '':
		font_kanji = aa;
		altuni = font[charToUnicode(font_kanji)].altuni;
		for kanji in cc:
			if altuni == None:
				altuni = ((charToUnicode(kanji),-1,0),);
			else:
				altuni = altuni +((charToUnicode(kanji),-1,0),);
		font[charToUnicode(font_kanji)].altuni = altuni;

for kanjis in kanji_123_k:#严
	kanji_unicode = charToUnicode(kanjis[0]);
	if kanji_unicode in font:
		if font[kanji_unicode].unicode == kanji_unicode:
			altuni = font[kanji_unicode].altuni;
			for kanji in kanjis:
				if not charToUnicode(kanji) in font:
					if altuni == None:
						altuni = ((charToUnicode(kanji),-1,0),);
					else:
						altuni = altuni +((charToUnicode(kanji),-1,0),);
			font[kanji_unicode].altuni = altuni;

for kanjis in kanji_1:#严
	aa = '';#主
	cc = '';#从
	for kanji in kanjis:
		kanji_unicode = charToUnicode(kanji);
		if not kanji_unicode in font:
			cc += kanji;
		else:
			if aa == '':
				if font[kanji_unicode].unicode == kanji_unicode:
					aa = kanji;
	if  cc != '' and aa != '':
		font_kanji = aa;
		altuni = font[charToUnicode(font_kanji)].altuni;
		for kanji in cc:
			if altuni == None:
				altuni = ((charToUnicode(kanji),-1,0),);
			else:
				altuni = altuni +((charToUnicode(kanji),-1,0),);
		font[charToUnicode(font_kanji)].altuni = altuni;

#这一步可取消。
for kanjis in kanji_123_k:#宽
	aa = '';#主
	bb = '';#副
	cc = '';#从
	for kanji in kanjis:
		kanji_unicode = charToUnicode(kanji);
		if not kanji_unicode in font:
			cc += kanji;
		else:
			if aa == '':
				if font[kanji_unicode].unicode == kanji_unicode:
					aa = kanji;
				else:
					if bb == '':
						bb = kanji;
	if  cc != '' and (aa != '' or bb != ''):
		if aa != '':
			font_kanji = aa;
		else:
			font_kanji = bb;
		altuni = font[charToUnicode(font_kanji)].altuni;
		for kanji in cc:
			if altuni == None:
				altuni = ((charToUnicode(kanji),-1,0),);
			else:
				altuni = altuni +((charToUnicode(kanji),-1,0),);
		font[charToUnicode(font_kanji)].altuni = altuni;


font_name = fontfile[:-4];
font_name_ext = fontfile[-4:];

#print('save '+font_name+'_uu.sfd ......');
#font.save(font_name+'_uu.sfd');
#font.close();
#del font;
#font = fontforge.open(font_name+'_uu.sfd');
print('generate '+font_name+'_uu'+font_name_ext+' ......');
font.generate(font_name+'_uu'+font_name_ext,"",("round","apple","opentype","dummy-dsig"));