% python combine.py csv/dt_1_3.csv csv/dt_5_6.csv csv/dt_final.csv
% python combine2.py csv/misc_1_3.csv csv/misc_3_5.csv csv/misc_1_5.csv
% python combine2.py csv/misc_1_5.csv csv/misc_5_6.csv csv/misc_final.csv
////// BELOW NUMBERS VARY BASED ON HOW MANY DT SAMPLES THERE ARE //////
% python sample.py csv/misc_final.csv csv/misc_250.csv 250
% python sample.py csv/misc_final.csv csv/misc_100.csv 100
% python combine3.py csv/misc_250.csv csv/dt_final.csv csv/train.csv
% python combine3.py csv/misc_100.csv csv/dt_3_5.csv csv/test.csv
% python main.py csv/train.csv model_dt.pkl --test_file csv/test.csv --test_output predictions.csv
