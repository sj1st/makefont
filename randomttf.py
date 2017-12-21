#!D:/green/ff171019_3/bin/ffpython.exe
# -*- coding: UTF-8 -*-
#"D:/green/ff171019_3/bin/fontforge" -script randomttf.py a.ttf b.ttf c.ttf
#随机选择字体字形，生成一个字体。
import os,fontforge,sys,random;

argvn = len(sys.argv); #4
gns = [];
i = 2;
while (i < argvn): #2 3
	gns.append([]); #0 1
	i += 1;

font1 = fontforge.open(sys.argv[1]);
if font1.is_cid : font1.cidFlatten();
print(sys.argv[1] + ' OK');
for glyph in font1.glyphs():
	layer = glyph.foreground; #字形的前景层
	if not layer.isEmpty() : #字形不是空的
		glyphname = glyph.glyphname;
		id = random.randint(0,argvn-2);#0 1 2
		if (id != (argvn-2)) : gns[id].append(glyphname);
print('Random OK');
i = 2;
while (i < argvn): #2 3
	font = fontforge.open(sys.argv[i]);
	if font.is_cid : font.cidFlatten();
	for glyphname in gns[i-2]: #0 1
		if (glyphname in font):
			font1[glyphname].foreground = font[glyphname].foreground;
			font1[glyphname].left_side_bearing = font[glyphname].left_side_bearing;
			font1[glyphname].width = font[glyphname].width;
	font.close();
	print(sys.argv[i] + ' OK');
	i += 1;

font_ext = sys.argv[1][-4:];
print('generate ......');
font1.generate('randomttf'+font_ext,"",("round","apple","opentype","dummy-dsig"));
font1.close();