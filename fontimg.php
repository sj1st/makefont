<?php
/*
fontimg.php fontname size

50%
$00-$1f
$20,$a0
$3000
*/
require __DIR__ . '/config/com.php';

$condir = __DIR__ . '/config/';
$downdir = 'D:/font/fontimg/';
/*
fontimg('st01',600);
fontimg('ht01',600);
fontimg('kt01',600);
fontimg('fs01',600);
fontimg('wb01',600);
fontimg('xk01',600);
*/

fontimg($argv[1],intval($argv[2]));

function fontimg($fontid,$size){
	Global $condir, $downdir;
	
	$font = __DIR__ . '/'.$fontid.'.ttf';
	$linenum = 1; //行数
	$buffer = '';//初始化
	$delmd5 = file_get_contents($condir.'md5.txt');//重复文件的md5
	$amd5 = '';
	$samemd5i = 0;
	
	$filedir =$downdir.$fontid.'/';
	$filedirx =$downdir.$fontid.'x/';
	mkdirs($filedir);
	mkdirs($filedirx);

	$handle = @fopen($condir . 'gb2312.txt', 'r'); //每个字unicode为一行
//	$handle = @fopen($condir . 'test.txt', 'r'); //每个字unicode为一行
	if (!$handle) die('error');
	while (!feof($handle)) {
		$buffer = rtrim(fgets($handle));
		$unicode = hexdec($buffer);
		$char = CodeToChar($unicode);
		$filepathname = $filedir . $buffer . '.png';
		$filepathnamex = $filedirx . $buffer . '.png';
		if (file_exists($filepathname) || file_exists($filepathnamex)) {
			echo $linenum,"\n";
			$linenum++; //行数

			if(file_exists($filepathname)){
				$imd5 = md5_file($filepathname);
				if(strpos($delmd5, $imd5) !== false){
					unlink($filepathname);
					file_put_contents($filepathnamex,'');//新建空文件
					echo 'move...........................' . "\n";
				}else{
					if($amd5 == $imd5){
						$samemd5i += 1;
						if($samemd5i > 10){
							$delmd5 .= ',' . $amd5;
							file_put_contents($condir.'md5.txt', ',' . $amd5, FILE_APPEND);
							$amd5 = '';
							$samemd5i = 0;
						}
					}else{
						$amd5 = $imd5;
						$samemd5i = 1;
					}
				}
			}
			
			
		} else {
			echo  $linenum . ':' . $buffer,' ';

			$ttfbox = imagettfbbox($size,0,$font, $char);
			$ttfbox = implode(',',$ttfbox);
			if($ttfbox != '0,0,0,0,0,0,0,0'){
				echo $ttfbox ,"\n";
				$img = imagecreatetruecolor(1200, 1200);//创建空白图片
				$white = imagecolorallocate($img, 255, 255, 255);
				$black = imagecolorallocate($img, 0, 0, 0);
				imagefill($img, 0, 0, $white);
				imagettftext($img, $size, 0, 200, 900, $black, $font, $char);
				imagepng($img,$filepathname);
				imagedestroy($img);

				$imd5 = md5_file($filepathname);
				if(strpos($delmd5, $imd5) !== false){
					unlink($filepathname);
					file_put_contents($filepathnamex,'');//新建空文件
					echo 'move...........................' . "\n";
				}else{
					if($amd5 == $imd5){
						$samemd5i += 1;
						if($samemd5i > 10){
							$delmd5 .= ',' . $amd5;
							file_put_contents($condir.'md5.txt', ',' . $amd5, FILE_APPEND);
							$amd5 = '';
							$samemd5i = 0;
						}
					}else{
						$amd5 = $imd5;
						$samemd5i = 1;
					}
				}
			}else{
				echo "......\n";
			}
				
			$linenum++; //行数
		}
	}
	fclose($handle);
	
	date_default_timezone_set('Etc/GMT-8');
    echo $fontid," over.\n";
    echo (date(DATE_ATOM, time())),"\n\n";
}

