set title "Space time trajectory diagram"
set xlabel "Time Horizon"
set ylabel "Space (distance)"  offset -1
set xtics (" 0:00" 0 ," 1:00" 60 ," 2:00" 120 ," 3:00" 180 ," 4:00" 240 ," 5:00" 300 ," 6:00" 360 ," 7:00" 420 ," 8:00" 480 ) 
set ytics (" " 0)
set xrange [0:481] 
set yrange [0:60.00] 
plot "agent1.txt" using 1:2 title 'agent 1'  with lines,\
"agent2.txt" using 1:2 title 'agent 2'  with lines
