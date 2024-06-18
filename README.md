# PageRank
A Python project using AI to simulate Google's PageRank algorithm, which is used to decide how "important" a website is based on how many "important" websites it links to. This was submitted for the CS50 AI Harvard course.

    NOTE: Some setup is required. Pages are not implemented for you. Setup section below

Importance is decided using two different methods.

Method 1: Brute force 
Basically determines how likely a person clicking links at random is to stumble upon your website
1. Start at a random page in the dataset, also referred to as the corpus
3. Select one of the pages that it links to at random
4. Or with a d% chance (in this case, 15%), pick any random website from the corpus (to prevent 2 websites from linking to each other over and over again)
5. add (1/N) to the pagerank (where N is the amount of samples. In this case, N = 10,000)
6. Repeat N times
7. All PageRanks should add up to 1.

Method 2: Recursive
It produces virtually the same output, but it is better for datasets that may add new websites, as it uses pagerank to recursively calculate pagerank
1. Start by assigning every PageRank to 1/n (where n is the amount of pages in the corpus)
2. For every page in the corpus, set the PageRank equal to this formula:

        (1-d)/n + d(PageRank(i) / numLinks(i)) for all i in links)

        (1-d)/n --> random chance for someone to stumble upon this website (basically a default pagerank). In this case, set to 15%
        d --> multiply by .85 because there is a 85% chance for the person to not click a random page (where d is .85)
        i --> any website that links to the current website
        PageRank(i) --> how likely someone will be at i
        numLinks(i) --> how likely someone at i will go to the current website
        ^add d(PageRank(i) / numLinks(i)) for every i 

4. repeat this process until no PageRank changes more than a value of 0.001

5. all values will sum to 1

##Setup
1. add any HTML files to the "corpus" file
2. make sure some of them link to others, like seen in this exmple:

       <li><a href="EXAMPLE.html">EXAMPLE</a></li>
3. when running, pass the "corpus" file name into args[0] (python pagerank.py corpus)
