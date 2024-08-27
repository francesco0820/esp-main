 python combine.py csv/da_1_3.csv csv/da_5_6.csv csv/da_final.csv
 python combine2.py csv/misc_1_3.csv csv/misc_3_5.csv csv/misc_1_5.csv
 python combine2.py csv/misc_1_5.csv csv/misc_5_6.csv csv/misc_final.csv
////// BELOW NUMBERS VARY BASED ON HOW MANY DA SAMPLES THERE ARE //////
 python sample.py csv/misc_final.csv csv/misc_125.csv 125
python sample.py csv/misc_final.csv csv/misc_100.csv 100
 python combine3.py csv/misc_125.csv csv/da_final.csv csv/train.csv
 python combine3.py csv/misc_100.csv csv/da_3_5.csv csv/test.csv
python main.py csv/train.csv model_da.pkl --test_file csv/test.csv --test_output predictions.csv
