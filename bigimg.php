<?php
/*
規整圖片名稱，好 (2).png 变成 好.g1.png
统一图片尺寸，并加上定位点

运行时先执行 CHCP 65001
然后修改窗口属性，改变字体
在命令行标题栏上点击右键，选择"属性"->"字体"，将字体修改为True Type字体"Lucida Console"，然后点击确定将属性应用到当前窗口。 
*/

//GD库

require __DIR__ . '/config/com.php';

$condir = __DIR__ . '/config/';
$downdir = 'D:/font/tool/';

bigimg($argv[1]);

function bigimg($imgid){
//字体编号；最小点尺寸，最大点尺寸,线外,点数率
//线外:[0,1]比率 (-,0)披 (1,+)壳
	Global $condir, $downdir;
	
	$dir =$downdir.$imgid.'/';
	$dirp =$downdir.$imgid.'_t/';
	
	mkdirs($dirp);
	
	$max_width = 0;
	$max_height = 0;
	
	if(is_dir($dir)){
		if($dh = scandir($dir,1)){
			
			$j = 1;
//*
			foreach ($dh as $file){
				if(!($file == '.' || $file == '..')){
					$filefull = $dir.$file;
					if(is_file($filefull)){

						$im = imagecreatefrompng($filefull);
						
						$max_width = max($max_width, imagesx($im));
						$max_height = max($max_height,imagesy($im));
						
						imagedestroy($im);
						
						echo $j,' OK',"\r\n";
						$j++;
						
					}
				}
			}
			
			$max_width += 100;
			$max_height += 100;
/*/
			$max_width = 902;
			$max_height = 702;
//*/
			echo $max_width,',',$max_height,"\n";
			$j = 0;
			foreach ($dh as $file){
				if(!($file == '.' || $file == '..')){
					$filefull = $dir.$file;
					if(is_file($filefull)){
						
						$img = imagecreatetruecolor($max_width, $max_height);//创建空白图片
						$white = imagecolorallocate($img, 255, 255, 255);
						$black = imagecolorallocate($img, 0, 0, 0);
						imagefill($img, 0, 0, $white);//底色白色
						imagefilledrectangle($img, 0, 0, 50, 50, $black);
						imagefilledrectangle($img, $max_width-51, $max_height-51, $max_width-1, $max_height-1, $black);

						$im = imagecreatefrompng($filefull);

						$width = imagesx($im);
						$height = imagesy($im);

						$dst_x = round(($max_width - $width)/2);
						$dst_y = round(($max_height - $height)/2);
						
						imagecopy ($img, $im, $dst_x, $dst_y, 0, 0, $width, $height);
						imagedestroy($im);//释放原图
						
						//$file=iconv('GBK','UTF-8', $file);
						
						
						$str = (explode('.',$file))[0];//获得主字
						$str = (explode(' ',$str))[0];//获得主字
						
						echo $str,"\n";
						
						$i = 1;
						$newfile = $dirp.$str;
						
						//$newfile=iconv('UTF-8','GBK', $newfile);
						
						if(file_exists($newfile.'.png')){
							//存在主图
							while (file_exists($newfile.'.g'.strval($i).'.png')) {
								$i += 1;
							}
							imagepng($img,$newfile.'.g'.strval($i).'.png');//保存
						}else{
							//不存在主图
							imagepng($img,$newfile.'.png');//保存
						}
						
						imagedestroy($img);//释放新图
						
						echo $j++;
						
					}
				}
			}

		}
	}
}