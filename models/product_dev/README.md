% python combine.py csv/pd_1_3.csv csv/pd_5_6.csv csv/pd_final.csv
% python combine2.py csv/misc_1_3.csv csv/misc_3_5.csv csv/misc_1_5.csv
% python combine2.py csv/misc_1_5.csv csv/misc_5_6.csv csv/misc_final.csv
////// BELOW NUMBERS VARY BASED ON HOW MANY PD SAMPLES THERE ARE //////
% python sample.py csv/misc_final.csv csv/misc_300.csv 300
% python sample.py csv/misc_final.csv csv/misc_150.csv 150
% python combine3.py csv/misc_300.csv csv/pd_final.csv csv/train.csv
% python combine3.py csv/misc_150.csv csv/pd_3_5.csv csv/test.csv
% python main.py csv/train.csv model_pd.pkl --test_file csv/test.csv --test_output predictions.csv
