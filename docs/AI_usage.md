# Evaluation of Generative AI Usage
## Overview
adsf
## Example 1: URL Normalisation
#### Prompt
What conditions should a web crawler check for when normalising a URL to prevent duplicate visits?

#### Output Summary
The AI suggested removing fragments and adding a trailing slashes to URLs that do not point towards files, suggestig urllib for parsing.

#### Evaluation
This was very useful as I would not have thought to leave trailing slashes from file URLs, and getting normalisation correct is very important for crawler accuracy through avoiding duplicate detections. I therefore implemented the AI's suggestions. This helped me to reinforce my normalisation logic, as well as reminding me that even when I have a general understanding of why/how something should be implemented, generative AI may be able to help me see things I may have missed.

## Example 2: Link extraction
#### Prompt
What is the best approach to extracting the URLs of links from HTML for a web crawler?

#### Output Summary
The AI recommended the use of BeautifulSoup to find anchor tags and urljoin to generate absolute URLs from relative ones, providing code demonstrating how to do this.

#### Evaluation
The recommendations and instructions were very useful, and I was able to adapt the code for my own use. However, the proposed solution did not incorporate logic for URL normalisation or ignoring external URLs, so I had to incorporate the logic from my other subroutines into this one. This suggests that AI generated code can be very useful in progressing your work and finding solutions to problems, but it must often be adapted to satisfy specific requirements.

## Example 3: Visible Text
#### Prompt
I wish to extract just the visible text from a web page for the sake of web crawling. What HTML elements should I ignore?

#### Output Summary
The output clearly indicated that I should use BeautifulSoup to parse the HTML, removing 'script', 'style', and 'noscript' elements, then extracting the page title and visible text.

#### Evaluation
I believe that this is an area in which AI exceeds. It is only a quick and simple prompt, but when I tried to google it, I could not find the answer. AI is able to use context and supporting materials to answer highly specific questions - an area where search browsers lack. Another prompt I used on this topic was to generate example HTML that I could use for testing, saving me time and improving efficiency.

## Example 4: Output Structure
#### Prompt
What data should a small python crawler return for crawled pages before passing them to an indexer?

#### Output Summary
The AI suggested that a dataclass with fields for URL, title, and visible text should be returned.

#### Evaluation
The AI is able to see that a dataclass gives clearer structure than tuples while still remaining very simple, and it also confirmed that I was not missing any important information other than URL, title, and visible text. While this prompt was not very consequential in affecting my decisions, it did confirm my choices to me, and allowed me to reinforce my learning through development.

## Example 5: Fetching Testing Strategy
#### Prompt
How should I implement controlled unit tests for a subroutine that fetches a page without having to connect to live active web servers?

#### Output Summary
Implementing a FakeResponse and a FakeGet to simulate real crawling behaviour makes unit testing simpler, faster, and more reliable. However, it is important to also test the crawler's ability on live websites, once the unit testing has been passed. The process of implementing this fake response was explained.

#### Evaluation
This was a creative solution to a problem that I most likely would not have thought of. It also helped me understand that testing code relying on proper network traffic introduces lots of unreliable noise, and controlled testing should ensure that the processes work as expected before testing on a live website.