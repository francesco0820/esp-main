# Docker Installation available under esp-main





#how to push to github everytime you make a change
git add .
git commit -m "insert message here"
git push 

#how to compile and run a python file
python filename

#how to upload users
rename old execs.csv file oldexecs.csv
put the new execs CSV file into website > data > call it execs.csv

#how to upload the records
rename old data CSV file olddata.csv
put the CSV file into website > data > call it data.csv

#run the tagging models
#comment IN only one line at a time
python run.py
#comment IN the next line

#edit the insights page
go to esp > templates > insights.html
follow guides from comments (lines 23-94)

#run/deploy the website
cd website
./bin/espdb create
./bin/esprun
control z to kill
lsof -i:8000
kill -9 ____ for every port that shows up in the terminal(ex:9987)

#to go to the website in any browser
localhost:8000
