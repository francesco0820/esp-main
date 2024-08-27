python combine.py csv/hcd_1_3.csv csv/hcd_3_5.csv csv/hcd_1_5.csv
python combine.py csv/hcd_1_5.csv csv/hcd_5_6.csv csv/hcd_final.csv
python combine2.py csv/misc_1_3.csv csv/misc_3_5.csv csv/misc_1_5.csv
python combine2.py csv/misc_1_5.csv csv/misc_5_6.csv csv/misc_final.csv
python sample.py csv/misc_final.csv csv/misc_100.csv 100
python combine3.py csv/misc_100.csv csv/hcd_final.csv csv/combined.csv
python split.py csv/combined.csv csv/train.csv csv/test.csv
python main.py csv/train.csv model_hcd3.pkl --test_file csv/test.csv --test_output predictions.csv
