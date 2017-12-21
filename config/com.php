<?php
ini_set('memory_limit','800M');

//建立多级目录
function mkdirs($dir){
	if(!is_dir($dir)){
		if (!mkdirs(dirname($dir)))
			return false;
		if (!mkdir($dir,0777))
			return false;
	}
	return true;
}

function charToCode($word,$encoding='UTF-32') {
	//返回诸如 0x91D1
	/* 设置内部储存字符编码为 UTF-8 */
	mb_internal_encoding('UTF-8');

	if(mb_strlen($word) > 1){
		$word = mb_substr($word,0,1);
	}

	if(strlen($word) == 1){
		return ord($word);
	}

	return intval(bin2hex(mb_convert_encoding($word, $encoding, 'UTF-8')),16);
}

function CodeToChar($unicode,$encoding='UTF-32'){
	//储存内码为UTF8
	if($unicode < 0){ return '';}

	return mb_convert_encoding(hex2bin(str_pad(dechex($unicode),8,'0',STR_PAD_LEFT)), 'UTF-8', $encoding);
}

function codeToUTF8URL($unicode){
	//返回诸如 '%e6%b1%89'
	return  preg_replace('/(\w{2})/','%$1',bin2hex(CodeToChar($unicode)));

}

function UTF8URL($word) {
    //获取其字符的内部数组表示，所以本文件应用utf-8编码！
    return  preg_replace('/(\w{2})/','%$1',bin2hex($word));
}

//===================================================

function good($word) {
	
	$word = preg_replace('/\s/',' ',$word);
	$word = preg_replace('/\s{2,}/',' ',$word);
	$word = preg_replace('/ ([a-zA-Z])/','\\1',$word);
	
	$word = trim($word);
	
	return $word;
}

function yasuo($word) {
	
	$word = preg_replace('/\s/',' ',$word);
	$word = preg_replace('/\s{2,}/',' ',$word);
	
	$word = trim($word);
	
	$word = str_replace(' 0 ','O',$word);
	$word = str_replace('.5 ','N',$word);
	$word = str_replace(' -','F',$word);
	$word = str_replace('t-','E',$word);
	$word = str_replace('q-','G',$word);
	$word = str_replace('.5','W',$word);
	
	$word = str_replace('1 ','I',$word);
	$word = str_replace('2 ','U',$word);
	$word = str_replace('3 ','Y',$word);
	$word = str_replace('4 ','R',$word);
	$word = str_replace('5 ','X',$word);
	$word = str_replace('6 ','K',$word);
	$word = str_replace('7 ','J',$word);
	$word = str_replace('8 ','B',$word);
	$word = str_replace('9 ','P',$word);
	$word = str_replace('0 ','D',$word);
	return base64_encode(gzcompress($word ,9));

}

function jieya($word) {
	$word = gzuncompress(base64_decode($word));
	
	$word = str_replace('I','1 ',$word);
	$word = str_replace('U','2 ',$word);
	$word = str_replace('Y','3 ',$word);
	$word = str_replace('R','4 ',$word);
	$word = str_replace('X','5 ',$word);
	$word = str_replace('K','6 ',$word);
	$word = str_replace('J','7 ',$word);
	$word = str_replace('B','8 ',$word);
	$word = str_replace('P','9 ',$word);
	$word = str_replace('D','0 ',$word);
	
	$word = str_replace('O',' 0 ',$word);
	$word = str_replace('N','.5 ',$word);
	$word = str_replace('F',' -',$word);
	$word = str_replace('E','t-',$word);
	$word = str_replace('G','q-',$word);
	$word = str_replace('W','.5',$word);
	
	return $word;
}

