<?php
    class captchaGenerator
    {
        protected $data_dir = './img';

        public function __construct($data_dir) {
            $this->data_dir = $data_dir[-1] == '/' ? $data_dir : $data_dir.'/';
            if (!file_exists($data_dir)) {
                mkdir($data_dir, 0755, true);
            }
        }

        public function generateCaptcha($textColor,$backgroundColor,$imgWidth,$imgHeight,$letter_quantity=4,$noiceLines=0,$noiceDots=0,$noiceColor='#162453')
        {
            /* Settings */
            $text = substr(str_shuffle("abcdefghijklmnopqrstuvwyxz0123456789"),0,($letter_quantity));
            $filename = $text.'.png';
            $font = './arialceb.ttf';
            $textColor=$this->hexToRGB($textColor);
            $fontSize = 40;

            $image = imagecreatetruecolor($imgWidth, $imgHeight);
            $textColor = imagecolorallocate($image, $textColor['r'],$textColor['g'],$textColor['b']);

            $backgroundColor = $this->hexToRGB($backgroundColor);
            $backgroundColor = imagecolorallocate($image, $backgroundColor['r'],$backgroundColor['g'],$backgroundColor['b']);

            imagefill($image,0,0,$backgroundColor);
            list($x, $y) = $this->ImageTTFCenter($image, $text, $font, $fontSize);
            imagettftext($image, $fontSize, 0, $x, $y, $textColor, $font, $text);

            /* generating lines randomly in background of image */
            if($noiceLines>0){
                $noiceColor=$this->hexToRGB($noiceColor);
                $noiceColor = imagecolorallocate($image, $noiceColor['r'],$noiceColor['g'],$noiceColor['b']);
                for( $i=0; $i<$noiceLines; $i++ ) {
                    imagesetthickness($image, $i % 4 + 2);
                    imageline($image, mt_rand(0,$imgWidth), mt_rand(0,$imgHeight),
                        mt_rand(0,$imgWidth), mt_rand(0,$imgHeight), $noiceColor);
                }
            }

            /* generating the dots randomly in background */
            if($noiceDots>0){
                for( $i=0; $i<$noiceDots; $i++ ) {
                    imagefilledellipse($image, mt_rand(0,$imgWidth),
                        mt_rand(0,$imgHeight), 3, 3, $textColor);
                }
            }

            imagepng($image,$this->data_dir.$filename);
            imagedestroy($image);
            return $filename;
        }

        /*function to convert hex value to rgb array*/
        protected function hexToRGB($colour)
        {
            if ( $colour[0] == '#' ) {
                $colour = substr( $colour, 1 );
            }
            if ( strlen( $colour ) == 6 ) {
                list( $r, $g, $b ) = array( $colour[0] . $colour[1], $colour[2] . $colour[3], $colour[4] . $colour[5] );
            } elseif ( strlen( $colour ) == 3 ) {
                list( $r, $g, $b ) = array( $colour[0] . $colour[0], $colour[1] . $colour[1], $colour[2] . $colour[2] );
            } else {
                return false;
            }
            $r = hexdec( $r );
            $g = hexdec( $g );
            $b = hexdec( $b );
            return array( 'r' => $r, 'g' => $g, 'b' => $b );
        }


        /*function to get center position on image*/
        protected function ImageTTFCenter($image, $text, $font, $size, $angle = 8)
        {
            $xi = imagesx($image);
            $yi = imagesy($image);
            $box = imagettfbbox($size, $angle, $font, $text);
            $xr = abs(max($box[2], $box[4]))+5;
            $yr = abs(max($box[5], $box[7]));
            $x = intval(($xi - $xr) / 2);
            $y = intval(($yi + $yr) / 2);
            return array($x, $y);
        }

    }

    $data_size = $argv[1];
    $width = $argv[2];
    $height = $argv[3];
    $data_dir = empty($argv[4]) ? './img' : $argv[4];
    $captchaGen = new captchaGenerator($data_dir);
    $letter_quantity = 4;
    for ($i=0; $i<$data_size; $i++) {
        if ($i == $data_size/3 || $i == $data_size/3*2) {
            $letter_quantity += 1;
        }
        echo $captchaGen->generateCaptcha('#8c8c8c', '#fff', $width, $height, $letter_quantity, $letter_quantity, 150, "#707070").PHP_EOL;
    }
?>
