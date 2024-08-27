% python combine.py csv/i_1_3.csv csv/i_5_6.csv csv/i_final.csv
% python combine2.py csv/misc_1_3.csv csv/misc_3_5.csv csv/misc_1_5.csv
% python combine2.py csv/misc_1_5.csv csv/misc_5_6.csv csv/misc_final.csv
////// BELOW NUMBERS VARY BASED ON HOW MANY CC SAMPLES THERE ARE //////
% python sample.py csv/misc_final.csv csv/misc_310.csv 310
% python sample.py csv/misc_final.csv csv/misc_135.csv 135
% python combine3.py csv/misc_310.csv csv/i_final.csv csv/train.csv
% python combine3.py csv/misc_135.csv csv/i_3_5.csv csv/test.csv
% python main.py csv/train.csv model_i.pkl --test_file csv/test.csv --test_output predictions.csv
