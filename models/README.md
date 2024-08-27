How to make a new model:

1. Create a folder with the theme name under models
2. Within the folder, add another folder named "csv" [<theme_name> > csv]
3. Download all the posts tagged as the theme you want. If there are multiple months/ tables with the data, name them accordingly. ["dataJune.csv" "dataJuly.csv" etc]
4. Download all the posts NOT tagged as the theme you want. Again, if there are multiple months/ tables with the data, name them accordingly. ["notThemeDataJune.csv" "notThemeDataJuly.csv" etc]
5. Dump all necessary data files into the csv folder [<theme_name> > csv > dataJune.csv]
6. If there are multiple files for the THEME that need to be combined, duplicate combine.py from the aiml folder and put it in the new theme folder. [<theme_name> > combine.py]
7. If you completed step (6), go into combine.py and edit the following lines:
    - Line 11: The first part (before the :) is a potential "alternate name" for the theme you are on. If you have multiple spellings, multiple cases, etc. ("Ai machine learning" vs "AI Machine Learning"), put the alternate name in the first spot, followed by the actual theme name after the : [A GOOD EXAMPLE OF THIS BEING NECESSARY IS IN transactions > combine.py]
    - Line 30: 'AI or Machine Learning' --> '<theme_name>' [MAKE SURE THIS IS EXACTLY AS IT IS IN THE SECOND PART OF LINE 11]
8. If there are multiple files for the not theme data that you need to be combined, duplicate combine2.py from the aiml folder and put it in the new theme folder. [<theme_name> > combine2.py]
9. If you completed step (8), go into combine2.py and edit the following lines:
    - Line 11: Make it exactly the same as Line 11 from Step (7)
    - Line 30: 'Not AI or Machine Learning' --> 'Not <theme_name>'
10. Duplicate combine3.py from the aiml folder and put it in the new theme folder. [<theme_name> > combine3.py]
11. Go into combine3.py and edit the following lines:
    - Line 11: Make it exactly the same as Line 11 from Step (7) and (9)
12. Duplicate csv_utils.py from the aiml folder and put it in the new theme folder. [<theme_name> > csv_utils.py]
13. Duplicate sample.py from the aiml folder and put it in the new theme folder. [<theme_name> > sample.py]
14. Duplicate split.py from the aiml folder and put it in the new theme folder. [<theme_name> > split.py]
15. Duplicate main.py from the aiml folder and put it in the new theme folder. [<theme_name> > main.py]
16. Go into main.py and edit the following lines: 
    - Line 30: 'is_ai_ml' --> 'is_<theme_name>'
    - Line 30: 'AI or Machine Learning' --> '<theme_name>' [MAKE SURE IT IS SPELLED THE SAME AS THE THEME IN THE RAW DATA]
    - Line 51: 'is_ai_ml' --> 'is_<theme_name>' [MAKE SURE THIS IS THE SAME VARIABLE NAME AS LINE 30]
    - Line 59: 'is_ai_ml' --> 'is_<theme_name>' [MAKE SURE THIS IS THE SAME VARIABLE NAME AS LINE 30]
    - Line 69: 'is_ai_ml' --> 'is_<theme_name>' [MAKE SURE THIS IS THE SAME VARIABLE NAME AS LINE 30]
    - Line 71: 'is_ai_ml' --> 'is_<theme_name>' [MAKE SURE THIS IS THE SAME VARIABLE NAME AS LINE 30]
    - Line 71: 'AI or Machine Learning' --> '<theme_name>' [MAKE SURE IT IS SPELLED THE SAME AS THE THEME IN THE RAW DATA]
    - Line 73: 'is_ai_ml' --> 'is_<theme_name>' [MAKE SURE THIS IS THE SAME VARIABLE NAME AS LINE 30]
    - Line 79: 'is_ai_ml' --> 'is_<theme_name>' [MAKE SURE THIS IS THE SAME VARIABLE NAME AS LINE 30]
    - Line 80: 'is_ai_ml' --> 'is_<theme_name>' [MAKE SURE THIS IS THE SAME VARIABLE NAME AS LINE 30]
    - Line 87: 'is_ai_ml' --> 'is_<theme_name>' [MAKE SURE THIS IS THE SAME VARIABLE NAME AS LINE 30]
    - Line 113: 'AI or Machine Learning' --> '<theme_name>' [MAKE SURE IT IS SPELLED THE SAME AS THE THEME IN THE RAW DATA]

NOW YOU'RE GOOD TO RUN IT!!! 


#lines to add stopwords
# Download NLTK stopwords

nltk.download('stopwords')
 
# Load NLTK stopwords

nltk_stop_words = set(stopwords.words('english'))
 
# Load custom stopwords from filewithopen('stopwords.txt', 'r') as file:

    custom_stop_words = set(line.strip() for line in file)
 
# Combine NLTK stopwords with custom stopwords

stop_words = nltk_stop_words.union(custom_stop_words)
 
# Now `stop_words` contains both NLTK and custom stopwords
 
in main.py, this replaces lines 13-15
 

