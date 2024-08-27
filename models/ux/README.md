% python combine.py csv/ux_3_5.csv csv/ux_5_6.csv csv/ux_final.csv
% python combine2.py csv/misc_1_3.csv csv/misc_3_5.csv csv/misc_1_5.csv
% python combine2.py csv/misc_1_5.csv csv/misc_5_6.csv csv/misc_final.csv
////// BELOW NUMBERS VARY BASED ON HOW MANY UX SAMPLES THERE ARE //////
% python sample.py csv/misc_final.csv csv/misc_75.csv 75
% python sample.py csv/misc_final.csv csv/misc_35.csv 35
% python combine3.py csv/misc_75.csv csv/ux_1_3.csv csv/train.csv
% python combine3.py csv/misc_35.csv csv/ux_final.csv csv/test.csv
% python main.py csv/train.csv model_ux.pkl --test_file csv/test.csv --test_output predictions.csv
