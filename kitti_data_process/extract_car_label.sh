#!/bin/sh  

kitti_path="/media/yangshun/0008EB70000B0B9F/Datasets/KITTI/data_object_image_2/KITTI" #path to kitti dataset
kitti_label_path="$kitti_path/training/label_2"         #path to the labels of kitti
kitti_car_label_path="$kitti_path/training/label_2car_newzai"  #path to the labels of cars in kitti

cd $kitti_label_path
if [ ! -d $kitti_car_label_path ];then
mkdir $kitti_car_label_path		
for file_a in ${kitti_label_path}/*.txt; do  
    temp_file=`basename $file_a`  
    cat $temp_file | while read line 
    do
    	type_name=`basename ${line%% *}`
	 if [ "$type_name" = "Car" ]
	 then 	
	     echo $line >> "$kitti_car_label_path/$temp_file"
	 fi
    done
done  
fi