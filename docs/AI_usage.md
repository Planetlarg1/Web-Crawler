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