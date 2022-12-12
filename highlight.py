import fitz
import re
import sys
from fuzzysearch import find_near_matches

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

#Remove protected spaces
text_list = [w.replace('\xa0', '') for w in text_list]


#Remove empty elements
text_list = list(filter(None, text_list))

#Print number of highlights in text_list
print(str(len(text_list)) + " highlights found in clippings")

#Highlighting:
#Load Document
doc = fitz.open(filename)

# Initiate list for results found by page.search_for
match = []

# Iterate over each page in the PDF and search for each highlight in the list
for page in doc:
    for text in text_list:
        # Use fuzzysearch find_near_matches to find close matches to the highlight text
        close_matches = find_near_matches(text, page.get_text(),max_l_dist=15)
        matched_substrings = [match.matched for match in close_matches]
        # Iterate over the close matches and add a highlight annotation for each one
        for matched in matched_substrings:
            rl = page.search_for(matched, quads = True)
            page.add_highlight_annot(rl)
            # Add the close matches to the match object
            if rl != []:
                match = match + [matched]

# Print how many matches were found
print(str(len(match)) + " instances highlighted in pdf")

# save to a new PDF at the end after annotating everything
doc.save(filename.rsplit( ".", 1 )[ 0 ] + "_annotated.pdf")

#Find the items that were not annotated by comparing text_list against match
#Since the implementation of fuzzy search there's a problem with matches containing newlines (\n). Even if they are listed here, they are annotated in the text.
print("These quotes could not be highlighted in the PDF:\n")
print(set(text_list) ^ set(filter(lambda x: not re.search(r'\n', x), match)))
