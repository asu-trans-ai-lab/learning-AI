set title "Dynamic Density Contour (Path 1 ) Unit: veh/mile/lane" 
set xlabel "Time Horizon"
set ylabel "Space (Node Sequence)"  offset -1
set xtics (" 0:00" 0 ," 2:00" 120 ," 4:00" 240 ," 6:00" 360 ," 8:00" 480 ,"10:00" 600 ,"12:00" 720 ,"14:00" 840 ,"16:00" 960 ,"18:00" 1080 ,"20:00" 1200 ,"22:00" 1320 ,"24:00" 1440 ) 
set ytics ("1" 0, "3" 10, "4" 20, "5" 30, "6" 40, "7" 50)
set xrange [0:1441] 
set yrange [0:50] 
set palette defined (0 "white", 10 "green", 30 "yellow", 50 "red")
set pm3d map
splot 'C:\GitHub\learning-transportation-engineering-and-traffic-analysis\undergraduate_student_project\data_sets_GMNS0.9\03_three_corridor\export_path_density.txt' matrix notitle
