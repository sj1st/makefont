#!D:/green/ff171019_3/bin/ffpython.exe
# -*- coding: UTF-8 -*-
#"D:/green/ff171019_3/bin/fontforge" -script ovwh.py x.ttf f.ttf
#套用模版字体的字形宽高信息		x.ttf是需要修改的字体	f.ttf是模版
import os,fontforge,sys;

x_font_file = sys.argv[1];#要修改的字体
x_font = fontforge.open(x_font_file);
x_em = x_font.em;#units_per_em

f_font_file = sys.argv[2];#模版字体
f_font = fontforge.open(f_font_file);
f_em = f_font.em;

#遍历字形
for glyph in x_font.glyphs():
	if glyph.unicode != -1 :
		if (
			(glyph.unicode >= 0x4E00 and glyph.unicode <= 0x9FFF) or #中日韩统一表意文字
			(glyph.unicode >= 0x3400 and glyph.unicode <= 0x4DBF) or #中日韩统一表意文字扩展A区
			(glyph.unicode >= 0x20000 and glyph.unicode <= 0x2A6DF) or #中日韩统一表意文字扩展B区
			(glyph.unicode >= 0x2A700 and glyph.unicode <= 0x2EBEF) or #中日韩统一表意文字扩展C\D\E\F区
			(glyph.unicode >= 0xF900 and glyph.unicode <= 0xFAFF ) or #中日韩兼容表意文字
			(glyph.unicode >= 0x2F800 and glyph.unicode <= 0x2FA1F ) or #中日韩兼容表意文字补充
			(glyph.unicode in [0x3005,0x3006,0x3007,0x3021,0x3022,0x3023,0x3024,0x3025,0x3026,0x3027,0x3028,0x3029,0x3038,0x3039,0x303A]) or
			(glyph.unicode >= 0x2F00 and glyph.unicode <= 0x2FDF ) or #康熙部首
			(glyph.unicode >= 0x2E80 and glyph.unicode <= 0x2EFF ) or #中日韩汉字部首补充
			(glyph.unicode >= 0x31C0 and glyph.unicode <= 0x31EF ) #中日韩笔画 
		):
			layer = glyph.foreground;#字形的前景层
			if not layer.isEmpty() : #字形不是空的
				if glyph.unicode in f_font : #模版字体有此码位
					f_glyph = f_font.createChar(glyph.unicode);
					x_box = glyph.boundingBox();  #[x_min, y_min, x_max, y_max]
					f_box = f_glyph.boundingBox();#[    0,     1,     2,     3]

					#先缩放
					scale_x = (f_box[2] - f_box[0])/(x_box[2] - x_box[0]) *(x_em/f_em);#x方向
					scale_y = (f_box[3] - f_box[1])/(x_box[3] - x_box[1]) *(x_em/f_em);#y方向
					scale_psMat = psMat.scale(scale_x,scale_y);
					glyph.transform(scale_psMat);#执行字形变换
					
					n_box = glyph.boundingBox();  #新位置
					
					#再移动
					#translate_x = (x_box[2] + x_box[0])/2 - (n_box[2] + n_box[0])/2;#x方向
					#translate_y = (x_box[3] + x_box[1])/2 - (n_box[3] + n_box[1])/2;#y方向
					
					translate_x = (f_box[2] + f_box[0])/2*(x_em/f_em) - (n_box[2] + n_box[0])/2;#x方向
					translate_y = (f_box[3] + f_box[1])/2*(x_em/f_em) - (n_box[3] + n_box[1])/2;#y方向
					
					translate_psMat = psMat.translate(translate_x,translate_y);
					glyph.transform(translate_psMat);#执行字形变换

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
print('generate '+x_font_file_name+'_wh'+x_font_file_name_ext+' ......');
x_font.generate(x_font_file_name+'_wh'+x_font_file_name_ext,"",("round","apple","opentype","dummy-dsig"));

x_font.close();
del x_font;