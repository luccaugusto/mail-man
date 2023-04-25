#!/bin/sh

generated_images=""
image_number=""
data_dir="./img"
height=""
width=""

wave_transform()
{
	image="$1"
	wave_prefix="wave-"
	crop_prefix="crop-"
	width_distortion=$((RANDOM % 200 + 100))
	distort_rate=$((RANDOM % 30 + 18))
	height_distortion=$((width_distortion / distort_rate))

	convert "$data_dir/$image" -wave "$height_distortion""x""$width_distortion" "$data_dir/$wave_prefix$image"
	convert "$data_dir/$wave_prefix$image" -crop "$width""x""$height" "$data_dir/$crop_prefix$image"
	rm "$data_dir/$wave_prefix$image"

	if [ -f "$data_dir/$crop_prefix$image" ]
	then
		mv "$data_dir/$crop_prefix$image" "$image"
	else
		extension=${image##*.}
		filename=${image%%.*}
		mv "$data_dir/$crop_prefix$filename-0.$extension" "$data_dir/$image"
		rm $data_dir/$crop_prefix$filename-*
	fi
}

generate_captcha()
{
	generated_images=$(php captcha-gen.php "$1" "$2" "$3" "$4")
	generated_images=( $generated_images )
}

show_help()
{
	echo "Usage: ./generate-train-set.sh dataset_size width height [ data_dir ]"
}


if [ "$(basename "$0")" = "${SHELL##/bin/}" ]
then
	echo "Please run the script with './generate-train-set.sh' not 'sh generate-train-set.sh'"
else
	dataset_size=$1
	[ ! "$dataset_size" ] && show_help && exit
	shift
	width=$1
	[ ! "$width" ] && show_help && exit
	shift
	height=$1
	[ ! "$height" ] && show_help && exit
	[ "$2" ] && data_dir="$2"

	generate_captcha $dataset_size $width $height $data_dir

	for image in ${generated_images[@]}
	do
		wave_transform "$image"
	done
fi
