# -*- coding: UTF-8 -*-
#"D:/green/ff171019_3/bin/fontforge" -script ttf2png.py m.ttf
import os,fontforge,sys;

m_font_file = sys.argv[1];#字体

print('open ',m_font_file);
m_font = fontforge.open(m_font_file);



#产生字形
print('make png......');
for m_glyph in m_font.glyphs():
	m_glyph.export('png/'+ m_glyph.glyphname +'.png',1000,8);#导出图像
	print('png/'+ m_glyph.glyphname +'.png OK');
m_font.close();
