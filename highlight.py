import fitz
import re
import sys

# Filename as argument
filename = sys.argv[1]
clippings = sys.argv[2]

# Open Kindle clippings file. The clippings should only contain clippings for the book in question
f = open(clippings, "r")
content = f.read()

# Remove unneccesary information (two lines above timecode)
result = re.sub(r"(.*\n?)(.*?)\d\d:\d\d:\d\d\n*",  '\<endquote\>', content)

#Remove the lines demarcating annotations and turning them into quotation marks.
result = re.sub(r"\n?==========",  '', result)

# Turn string into list
text_list = result.split("\<endquote\>")

#Remove newlines
text_list = [w.replace('\n', '') for w in text_list]

#Remove empty elements
text_list = list(filter(None, text_list))

#Print number of highlights in text_list
print(str(len(text_list)) + " highlights found in clippings")

#Highlighting:
#Load Document
doc = fitz.open(filename)

# Initiate list for results found by page.search_for
match = []

#Iterate over pages
for page in doc:
# iterate through each text using for loop and annotate
    for text in text_list:
        rl = page.search_for(text, quads = True)
        page.add_highlight_annot(rl)
        #if a match was found, add it to match
        if rl != []:
            match = match + [text]

# Print how many matches were found
print(str(len(match)) + " instances highlighted in pdf")

# save to a new PDF at the end after annotating everything
doc.save(filename.rsplit( ".", 1 )[ 0 ] + "_annotated.pdf")

#Find the items that were not annotated by comparing text_list against match
print("These quotes could not be highlighted in the PDF:\n")
print(set(text_list) ^ set(match))
