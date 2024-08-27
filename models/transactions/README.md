python combine.py csv/t_3_5.csv csv/t_5_6.csv csv/t_final.csv
python combine2.py csv/misc_1_3.csv csv/misc_3_5.csv csv/misc_1_5.csv
python combine2.py csv/misc_1_5.csv csv/misc_5_6.csv csv/misc_final.csv
python sample.py csv/misc_final.csv csv/misc_150.csv 150
python combine3.py csv/misc_150.csv csv/t_final.csv csv/combined.csv
python split.py csv/combined.csv csv/train.csv csv/test.csv
python main.py csv/train.csv model_t3.pkl --test_file csv/test.csv --test_output predictions.csv
