set title "Space time trajectory diagram" 
set xlabel "Time Horizon"
set ylabel "Space (distance)"  offset -1
set xtics (" 0:00" 0 ," 2:00" 120 ," 4:00" 240 ," 6:00" 360 ," 8:00" 480 ,"10:00" 600 ,"12:00" 720 ,"14:00" 840 ,"16:00" 960 ,"18:00" 1080 ,"20:00" 1200 ,"22:00" 1320 ,"24:00" 1440 ) 
set ytics ("a" 0, "b" 3, "c" 4, "d" 5, "6" 6, "7" 7, "8" 8, "9" 9, "10" 10, "ff" 20)
set xrange [0:720] 
set yrange [0:20] 
plot "train1.txt" using 1:2 title 'train 1' with lines,\
"train2.txt" using 1:2 title 'train 2' with lines,\
"train3.txt" using 1:2 title 'train 3' with lines,\
"train4.txt" using 1:2 title 'train 4' with lines,\
"train5.txt" using 1:2 title 'train 5' with lines