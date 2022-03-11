# Maximal-Match
Given the input files (DFAs) and a string, we have to split the string into fragments, each fragment accepted by
one of the DFAs given as input, using maximal match. If we can't split the string, the program will signal
that by writing "No viable alternative at.." followed by the index of the character where all the DFAs rejected
the fragment and none of them accepted it at some point.
