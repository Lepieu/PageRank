import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus: dict, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #initializing variables given in equation to their values (so it's a little nicer)
    probabilities = dict()
    N = len(corpus)
    d = damping_factor
    numLinks = len(corpus[page])
    if numLinks == 0: numLinks = len(corpus)
    
    for i in corpus.keys():
        probabilities[i] = (1-d)/N 
        if i in corpus[page] or len(corpus[page]) == 0:
            probabilities[i] += d * (1/numLinks)

    return probabilities
    
    raise NotImplementedError


def sample_pagerank(corpus: dict, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #initializing variables given in equation to their values (so it's a little nicer)
    N = len(corpus)
    d = damping_factor
    pageRank = dict()
    keys = list(corpus.keys())
    
    for i in keys:
        pageRank[i] = 0
    
    page = random.choice(keys)
    for sample in range(1, n):
        
        pageRank[page] += (1/n)
        nextStates = transition_model(corpus, page, d)
        
        '''Random algorithm to choose next state: 
        Pick a random number, iterate through each possibility, 
        if the probability is greater than the random number generated, that becomes the next state. 
        If not, the next one is compared to the difference between the random number and the sum of every other choice 
        (basically, page 1 is if the random number is between 0 and p(1), page 2 is between p(1) and p(2), ...). 
        This effectively should make it so that it's a weighted random choice hopefully'''
        randomChoice = random.random()
        for i in list(nextStates.keys()): 
            if nextStates[i] > randomChoice: 
                page = i
                break
            randomChoice -= nextStates[i]

    return pageRank
    raise NotImplementedError


def iterate_pagerank(corpus: dict, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    keys = list(corpus.keys())
    N = len(corpus)
    d = damping_factor
    
    
    pageRanks = dict()
    for i in keys:
        pageRanks[i] = (1/N)
    
    maxChange = 0.001
    while maxChange >= 0.001:
        maxChange = 0
        for i in keys:
            difference = currentPageRank(corpus, pageRanks, d, i)
            pageRanks[i] += difference
            maxChange = max(maxChange, abs(difference))
    
    return pageRanks
    raise NotImplementedError

def currentPageRank(corpus: dict, pageRanks: dict, d, page):
    pageRank = (1-d)/len(corpus) #formula initial 1-d/N
    for i in corpus.keys():
        numLinks = len(corpus[i])
        if numLinks == 0: numLinks = len(corpus)
        if page in corpus[i] or len(corpus[i]) == 0:
            pageRank += d * (pageRanks[i])/(numLinks) #formula PR(i)/numLinks(i) --> importance of other site divided by chance of being picked
    return pageRank - pageRanks[page] #i can add the difference to pageRank so i can easily calculate the max difference

if __name__ == "__main__":
    main()
