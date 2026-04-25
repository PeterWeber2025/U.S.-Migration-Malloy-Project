# U.S.-Migration-Malloy-Project

### Overview
For my project I used Malloy + DuckDB to analyze data from the Internal Revenue Service detailing the movement of people between counties and states over the time period 2011 - 2021. With the hope of finding patterns, trends, and insights pertaining to how U.S. citizens migrate throughout the country.

The data I got from the IRS came in separate files for each year, after merging and cleaning the dataset I was left with 6 columns and 550,000+ rows of information, making this a hefty dataset. The data contained in each row is relatively simple, recording the origin and destination state + county, followed by the year and the net migration.

### My Interests
I started this project with a couple key points I wanted to determine:

- What states have the most inflows and outflows from migration.
- Are migration trends regional, or state specific.
- California has a reptuation for having large outflows, is this reputation warranted, and what states do people from California move to the most.
-How has state to state migration fluctuated over the decade I am analyzing.

### Key Findings
### 1.
Migration trends vary significantly from state to state and shouldn't be generalized to entire regions. Just because one state in a region sends large numbers of migrants to another region doesn't mean its neighboring states do the same. Each state has its own distinct migration profile, and broad regional patterns can obscure these differences.
### 2. 
Migration between states isn't a stable phenomena, it varies heavily from year to year, for this time period (2011 - 2021), 2015 was the year with least migration at slightly less than 2 million migrants, and 2017 was the largest year with over 4 million migrants.
### 3.
When people decide to move, they are far more likely to cross state lines entirely than to simply relocate within their current state. In other words, the decision to migrate is less about minor lifestyle adjustments or local dissatisfaction and more about pursuing fundamentally different opportunities, costs of living, or environments that their current state simply can't offer.
### 4.
States that send the most migrants out also tend to attract the most migrants in. This means the impact of people leaving or arriving is often overstated — focusing only on outflows ignores the offsetting effect of inflows, and vice versa. A state that appears to be "hemorrhaging" residents may simultaneously be drawing in large numbers of new ones, making the net effect far more modest than headline migration numbers suggest.

### So What?
Migration data is relevant to a wide range of people — urban planners, real estate developers, governments, and businesses For all of them, having an accurate picture of where people are moving, and in what numbers, is foundational to making good decisions. 

This analysis offers a correction to the oversimplified migration narratives that dominate public discourse. A state is rarely just "gaining" or "losing" peoplem net migration is what actually matters. In most high profile cases inflows and outflows largely offset each other, and migration fluctuates significantly year to year, making single-year snapshots a poor basis for sweeping conclusions.
