#!D:/green/ff171019_3/bin/ffpython.exe
# -*- coding: UTF-8 -*-
#"D:/green/ff171019_3/bin/fontforge" -script otfalt.py a.ttf
#otf异体字
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

kanji_all = charSis.kanji + charMe.kanji + charDau.kanji;


kanji_0 =[];#统合同字表
#合并同字条
kanji_0.append(kanji_all.pop());
while len(kanji_all) > 0:
	hanzis = kanji_all.pop();
	restart = False;#标记A
	for kanji in hanzis:#同字条总的汉字
		for i in range(len(kanji_0)):
			if kanji in kanji_0[i]:
				restart = True;#标记A
				kanji_0[i] = strSetStr(kanji_0[i]+hanzis);
				break;
		if restart:
			break;
	if not restart:
		kanji_0.append(hanzis);

#--------重复一次
kanji_all = kanji_0 + [];
kanji_0 =[];#统合同字表
#合并同字条
kanji_0.append(kanji_all.pop());
while len(kanji_all) > 0:
	hanzis = kanji_all.pop();
	restart = False;#标记A
	for kanji in hanzis:#同字条总的汉字
		for i in range(len(kanji_0)):
			if kanji in kanji_0[i]:
				restart = True;#标记A
				kanji_0[i] = strSetStr(kanji_0[i]+hanzis);
				break;
		if restart:
			break;
	if not restart:
		kanji_0.append(hanzis);

#--------再来一次
kanji_all = kanji_0 + [];
kanji_0 =[];#统合同字表
#合并同字条
kanji_0.append(kanji_all.pop());
while len(kanji_all) > 0:
	hanzis = kanji_all.pop();
	restart = False;#标记A
	for kanji in hanzis:#同字条总的汉字
		for i in range(len(kanji_0)):
			if kanji in kanji_0[i]:
				restart = True;#标记A
				kanji_0[i] = strSetStr(kanji_0[i]+hanzis);
				break;
		if restart:
			break;
	if not restart:
		kanji_0.append(hanzis);
		
		
fontfile = sys.argv[1];
font = fontforge.open(fontfile);

gNames =[];#异体字组

for kanjis in kanji_0:
	agNames = [];#一个异体字组
	for kanji in kanjis:
		unicode = charToUnicode(kanji);
		aname = 'uni'+((hex(unicode))[2:]).zfill(4).lower();
		for glyph_b in font.glyphs():
			if glyph_b.glyphname.lower().startswith(aname) :
				agNames.append(glyph_b.glyphname);
	if len(agNames) >1 :
			gNames.append(agNames);

file_object = codecs.open(fontfile+'.otf_alt.txt', 'w',"utf-8") ;

str = '''
script DFLT {
  # Default
	feature AccessAllAlternates;
}

script hani {
  # CJK Ideographic
	feature AccessAllAlternates;
}

feature AccessAllAlternates aalt {
	# 特征标签(备选字)
  lookup Alternate1;
}

lookup Alternate1 {
''';

file_object.write(str);

for agNames in gNames:
	for agName in agNames:
		agNamesx = agNames[:];
		agNamesx.remove(agName);
		str = '	sub '+ agName + ' -> [' + (' '.join(agNamesx)) + '];'+"\r\n";
		file_object.write(str);
file_object.write('}');
file_object.close();