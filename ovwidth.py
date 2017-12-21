#!D:/green/ff171019_3/bin/ffpython.exe
# -*- coding: UTF-8 -*-
#"D:/green/ff171019_3/bin/fontforge" -script ovwidth.py x.ttf o.ttf
#套用模版字体的字形宽度信息
import os,fontforge,sys;

aunicode = 0x254B;#0x6B7B

f_font_file = sys.argv[2];#模版字体
f_font = fontforge.open(f_font_file);
f_em = f_font.em;
f_xx = f_font[aunicode].boundingBox();

x_font_file = sys.argv[1];#要修改的字体
x_font = fontforge.open(x_font_file);
x_em = x_font.em;
x_xx = x_font[aunicode].boundingBox();


#基本参数
x_font.ascent = f_font.ascent *(x_em/f_em);
x_font.descent = f_font.descent *(x_em/f_em);

x_font.os2_typoascent = f_font.os2_typoascent *(x_em/f_em);
x_font.os2_typoascent_add = f_font.os2_typoascent_add *(x_em/f_em);
x_font.os2_typodescent = f_font.os2_typodescent *(x_em/f_em);
x_font.os2_typodescent_add = f_font.os2_typodescent_add *(x_em/f_em);
x_font.os2_typolinegap = f_font.os2_typolinegap *(x_em/f_em);

x_font.os2_use_typo_metrics = f_font.os2_use_typo_metrics *(x_em/f_em);

x_font.os2_winascent = f_font.os2_winascent *(x_em/f_em);
x_font.os2_winascent_add = f_font.os2_winascent_add *(x_em/f_em);
x_font.os2_windescent = f_font.os2_windescent *(x_em/f_em);
x_font.os2_windescent_add = f_font.os2_windescent_add *(x_em/f_em);

#先放大
scale = (f_xx[2] - f_xx[0])/(x_xx[2] - x_xx[0]) *(x_em/f_em);
if scale != 1:
	x_psMat = psMat.scale(scale);
	for glyph in x_font.glyphs():
		glyph.transform(x_psMat);

x_xx = x_font[aunicode].boundingBox();

#再提升
translate_x = (f_xx[2] + f_xx[0])/2*(x_em/f_em) - (x_xx[2] + x_xx[0])/2;#x方向
translate_y = (f_xx[3] + f_xx[1])/2*(x_em/f_em) - (x_xx[3] + x_xx[1])/2;#y方向

if (translate_x != 0) and (translate_y != 0):
	x_psMat = psMat.translate(translate_x,translate_y);
	for glyph in x_font.glyphs():
		glyph.transform(x_psMat);

for glyph in x_font.glyphs():
	if glyph.unicode != -1:
		f_glyph = f_font.createChar(glyph.unicode);
		glyph.left_side_bearing = f_glyph.left_side_bearing*(x_em/f_em);
		glyph.width = f_glyph.width*(x_em/f_em);

f_font.close();
del f_font;

x_font_file_name = x_font_file[:-4];
x_font_file_name_ext = x_font_file[-4:];

#print('save '+x_font_file_name+'_ov.sfd ......');
#x_font.save(x_font_file_name+'_ov.sfd');
#x_font.close();
#del x_font;

#x_font = fontforge.open(x_font_file_name+'_ov.sfd');
print('generate '+x_font_file_name+'_ov'+x_font_file_name_ext+' ......');
x_font.generate(x_font_file_name+'_ov'+x_font_file_name_ext,"",("round","apple","opentype","dummy-dsig"));

x_font.close();
del x_font;