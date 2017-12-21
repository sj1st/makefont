#!D:/green/ff171019_3/bin/ffpython.exe
# -*- coding: UTF-8 -*-
#"D:/green/ff171019_3/bin/fontforge" -script otflig.py a.ttf
#otf异体字
import os,fontforge,sys,codecs;
		
fontfile = sys.argv[1];
font = fontforge.open(fontfile);

file_object = codecs.open(fontfile+'.otf_lig.txt', 'w',"utf-8") ;

str = '''
script DFLT {
  # Default
	feature DiscretionaryLigatures;
}

script hani {
  # CJK Ideographic
	feature DiscretionaryLigatures;
}

feature DiscretionaryLigatures dlig {
	# 特征标签(dlig自由连字)
  lookup Ligatures;
}

lookup Ligatures {
''';

file_object.write(str);

for glyph in font.glyphs():
	if glyph.unicode != -1:
		if '.' not in glyph.glyphname:
			if (glyph.glyphname+'.g1') in font:
				file_object.write('	sub '+ glyph.glyphname + ' g1 -> ' +glyph.glyphname+".g1;\r\n");
			if (glyph.glyphname+'.g2') in font:
				file_object.write('	sub '+ glyph.glyphname + ' g2 -> ' +glyph.glyphname+".g2;\r\n");
			if (glyph.glyphname+'.g3') in font:
				file_object.write('	sub '+ glyph.glyphname + ' g3 -> ' +glyph.glyphname+".g3;\r\n");
			if (glyph.glyphname+'.g4') in font:
				file_object.write('	sub '+ glyph.glyphname + ' g4 -> ' +glyph.glyphname+".g4;\r\n");

file_object.write('}');
file_object.close();