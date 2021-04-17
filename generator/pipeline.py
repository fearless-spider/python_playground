"""
Read every line of the file.
Split each line into a list of values.
Extract the column names.
Use the column names and lists to create a dictionary.
Filter out the rounds you aren’t interested in.
Calculate the total and average values for the rounds you are interested in.
"""
file_name = "../emails/loh_cleaned.csv"
# Generator to read each line
lines = (line for line in open(file_name))
# Generator to split each line into a list
list_line = (s.rstrip().split(",") for s in lines)
# Column names
cols = next(list_line)
print(cols)
# Create dictionary where keys are column names
email_dicts = (dict(zip(cols, data)) for data in list_line)
print(next(email_dicts))
