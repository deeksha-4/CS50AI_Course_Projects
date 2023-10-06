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


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    d={}
    for i in corpus:
        d[i]=0
    l = corpus[page]
    if len(l)!=0:
        for i in l:
            d[i] = damping_factor/len(l)
        for i in d:
            d[i]+=(1-damping_factor)/len(corpus)

    else:
        for i in d:
            d[i] = 1/len(corpus)

    for i in d:
        d[i]=round(d[i], 7)
    return d
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    d={}
    l=[]
    for i in corpus:
        l.append(i)
        d[i]=0
    index = random.randint(0, len(l)-1)
    page = l[index]
    d[page]+=1
    c=1
    while(c<=n):
        model = transition_model(corpus, page, damping_factor)
        l1, l2=[], []
        for i in model:
            l1.append(i)
            l2.append(model[i])
        r = random.choices(l1, weights=l2, k=1)
        page=r[0]
        d[page]+=1
        c+=1
    sum=0
    for i in d:
        sum+=d[i]
    for i in d:
        d[i]/=sum
    return d
    raise NotImplementedError

def check(d, e):
    m = 0
    for i in d:
        m=max(m, abs(d[i]-e[i]))
    return m

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    d={}
    e={}
    for i in corpus:
        d[i] = 1/len(corpus)
        e[i] = -5
    while(check(d, e) >= 0.001):
        e = dict(d)
        for i in d:
            d[i]= (1-damping_factor)/len(corpus)
            s=0
            for j in corpus:
                if i in corpus[j]:
                    s+=e[j]/len(corpus[j])
                elif len(corpus[j])==0:
                    s+=e[j]/len(corpus)
            d[i]+=damping_factor*s
    sum=0
    for i in d:
        sum+=d[i]
    for i in d:
        d[i]/=sum
    return d

    raise NotImplementedError


if __name__ == "__main__":
    main()
