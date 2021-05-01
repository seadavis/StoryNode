# StoryNode

This repository contains code to generate new stories from knowledge graphs. 

# Implementation Status

See the project for the MVP project to-do's. As of May 1st 2020, this repo only does relation extraction.

# Directory Structure

src, contains the source code

* core - contains the core data structures required to get the relation extraction to work
* printing - takes care of printing relevant information from the data structures
* transforms - hold some basic functions required to change text sources.

Code Examples, contains references to Spacy experiments so I'll know how to implement the different components when the time comes. This also allows
me to see if the basic idea for an algorithm is going to work before going through the effort of implementing a clean version with all
of the auxillary data structures.

Test contains.... Tests. 

# Running the Tests

To run the tests all you need to do is run the command python3 main.py Text_Examples/Test_Sentences.txt, from the command line.
