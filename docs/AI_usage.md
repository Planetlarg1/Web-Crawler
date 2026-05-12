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