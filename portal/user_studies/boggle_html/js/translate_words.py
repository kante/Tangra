
file = open("words.js")
for line in file:
    print "all_words[   {0}   ] = {1} ;".format( line.split(",")[0]  , 1)
    
