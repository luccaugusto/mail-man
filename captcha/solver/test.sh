solved=0
misses=0
image_directory="./test"
for img in $(ls $image_directory)
do
	captcha="$(python solve_captcha.py "$image_directory/$img")"
	echo $captcha
	echo ${img%%.*}
	answer=${img%%.*}
	[ "$captcha" == "$answer" ] && solved=$((solved+1)) && echo "Solved $img :)"
	[ "$captcha" != "$answer" ] && misses=$((misses+1)) && echo "Failed $img :("
done

total=$((solved + misses))

echo "Solved $solved/$total"
echo "Failed $misses/$total"
echo "Success rate = $((solved / total))"
