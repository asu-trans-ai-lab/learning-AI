set title "Dynamic Speed Contour (Path 1 ) Unit: mph" 
set xlabel "Time Horizon"
set ylabel "Space (Node Sequence)"  offset -1
set xtics (" 0:00" 0 ," 2:00" 120 ," 4:00" 240 ," 6:00" 360 ," 8:00" 480 ,"10:00" 600 ,"12:00" 720 ,"14:00" 840 ,"16:00" 960 ,"18:00" 1080 ,"20:00" 1200 ,"22:00" 1320 ,"24:00" 1440 ) 
set ytics ("8.97" 0, "9.87" 13, "11.37" 29, "12.89" 46, "14.59" 66, " " 71)
set xrange [0:1441] 
set yrange [0:71] 
set palette defined (0 "white", 0.1 "red", 40 "yellow", 50 "green")
set pm3d map
splot 'C:\GitHub\learning-transportation-engineering-and-traffic-analysis\undergraduate_student_project\data_sets_GMNS0.9\12_California_405\export_path_speed.txt' matrix notitle
