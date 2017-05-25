#!/bin/bash

function get_last_dir() {
  path=$1

  array=( `echo $path | tr -s '/' ' '`)
  last_index=`expr ${#array[@]} - 1`
  echo ${array[${last_index}]}
  return 0
}

array=(computer domestic economy entertainment local sports world)

for gn in ${array[@]}; do
    echo $gn
    src_path="./yahoo_news_test/"
    src_path2=$src_path$gn
    for file in `\find $src_path2 -maxdepth 1 -type f`; do
       save_path="./yahoo_news_test_mecabed/"
       last_dir=`get_last_dir $file`
       save_path2=$save_path$gn/$last_dir
       mecab -E "" $file | cut -f 1 > $save_path2
       #echo -e \ >> $file
    done
done
