# Dataset: BuzzFeed News “Trending” Strip, 2018–2023

*A tribute to a trailblazing newsroom.*

[BuzzFeedNews.com](http://web.archive.org/web/*/https://www.buzzfeednews.com/) launched in July 2018 as the dedicated homepage for BuzzFeed News. (Previously, BuzzFeed’s news coverage was published on BuzzFeed’s main domain, `buzzfeed.com`.) One key feature of the site was its “Trending” strip, [curated by editors](https://techcrunch.com/2018/07/18/buzzfeed-news/) and highlighting up to eight articles at a time:

![Screenshot of the trending strip](misc/trending-strip-screenshot.png)

In mid-November 2018, a few months after the site launched, I wrote a [script to fetch that list of articles](scripts/fetch.py) and to save that information to a simple file. The script ran every five minutes (with occasional interruptions) until [the newsroom’s final day of operation in May 2023](https://www.buzzfeednews.com/article/buzzfeednews/buzzfeed-news-oral-history-2012-2023). This repository contains all the data the script collected, in raw and deduplicated forms.

> __Disclosure__: [I worked](https://www.jsvine.com/) for BuzzFeed’s news division from March 2014 to January 2022. I undertook this project on personal time and out of personal interest, using only the publicly-available homepage; nothing here should be considered to represent the views of BuzzFeed or BuzzFeed News.

## Raw data

The file [`data/bfn-trending-strip-raw.tsv.gz`](data/bfn-trending-strip-raw.tsv.gz) contains the raw data I collected. I have compressed it with `gzip`, which reduces the size from 390MB to 11MB. 

### Structure

The file contains 3.1 million rows, each representing *one article* observed *at one point in time*.

The file uses these columns:

- `timestamp`: The time (in [UTC](https://en.wikipedia.org/wiki/Coordinated_Universal_Time)) of the fetch. All articles from the same fetch will have the same timestamp.
- `position`: The article's [zero-indexed](https://en.wikipedia.org/wiki/Zero-based_numbering) position in the trending strip, from left to right.
- `text`: The text of the link used to highlight the article. Note: Sometimes the same article is associated with different text at different points in time.
- `url`: The link's URL. Note: Sometimes (although relatively rarely) the URL for the same underlying article changes over time.

> __Note__: Although the script generally ran every five minutes, there are some gaps in the data, accounting for roughly 3% of the total time period covered. These gaps owe to two main factors: technical complications (such as server downtime) and periods during which the website swapped out the trending strip with breaking news alerts, [single-story highlights](http://web.archive.org/web/20200827153649/https://www.buzzfeednews.com/), or other notices. Unfortunately, I did not have the foresight to collect data that would distinguish between those scenarios.

### Example data

Here are six rows of the dataset, from one particular point in time on [August 27, 2020](http://web.archive.org/web/20200827170042/https://www.buzzfeednews.com/):

| timestamp           |   position | text                      | url                                                                                                            |
|---------------------|------------|---------------------------|----------------------------------------------------------------------------------------------------------------|
| 2020-08-27T13:35:04 |          0 | Kenosha Protests          | https://www.buzzfeednews.com/article/ellievhall/kenosha-suspect-kyle-rittenhouse-trump-rally                   |
| 2020-08-27T13:35:04 |          1 | Xinjiang Internment Camps | https://www.buzzfeednews.com/article/meghara/china-new-internment-camps-xinjiang-uighurs-muslims               |
| 2020-08-27T13:35:04 |          2 | NBA                       | https://www.buzzfeednews.com/article/skbaer/milkwaukee-bucks-boycott-jacob-blake                               |
| 2020-08-27T13:35:04 |          3 | Hurricane Laura           | https://www.buzzfeednews.com/article/emmanuelfelton/hurricane-laura-could-lead-to-an-environmental-disaster-on |
| 2020-08-27T13:35:04 |          4 | RNC 2020                  | https://www.buzzfeednews.com/article/ryancbrooks/trump-white-house-rnc-backdrop                                |
| 2020-08-27T13:35:04 |          5 | Mike Pence                | https://www.buzzfeednews.com/article/salvadorhernandez/pence-dhs-officer-death-rnc-speech                      |

## Deduplicated data

Because the trending strip typically updated much less often than the script fetched the data, the raw data file contains much redundancy. I.e., two fetches, five minutes apart, often returned exactly the same data.

To simplify this redundancy, I've also [created](scripts/dedupe.py) a smaller data file that contains a deduplicated version of the data: [`data/bfn-trending-strip-deduped.tsv`](data/bfn-trending-strip-deduped.tsv). It contains roughly 60x fewer rows, and takes up roughly 50x less space (less than 8MB).

### Structure

The file contains 51,344 rows, each representing *one article* observed *across a range of time*.

The file uses the same core columns as the raw data, but replaces `timestamp` with `timestamp_first` and `timestamp_last`, which represent the first and last *consecutive* fetches the script saw *identical* data. If the positions, text, or URLs changed *at all*, the file begins a new set of entries.

> __Note__: If you need a precise accounting of the specific fetch timings within the timestamp ranges, please see the "Timestamps of all fetches" section below.

### Data sample

Here are six rows of the dataset, from one particular time range on [August 27, 2020](http://web.archive.org/web/20200827170042/https://www.buzzfeednews.com/):

| timestamp_first     | timestamp_last      |   position | text                      | url                                                                                                            |
|---------------------|---------------------|------------|---------------------------|----------------------------------------------------------------------------------------------------------------|
| 2020-08-27T13:35:04 | 2020-08-27T17:50:03 |          0 | Kenosha Protests          | https://www.buzzfeednews.com/article/ellievhall/kenosha-suspect-kyle-rittenhouse-trump-rally                   |
| 2020-08-27T13:35:04 | 2020-08-27T17:50:03 |          1 | Xinjiang Internment Camps | https://www.buzzfeednews.com/article/meghara/china-new-internment-camps-xinjiang-uighurs-muslims               |
| 2020-08-27T13:35:04 | 2020-08-27T17:50:03 |          2 | NBA                       | https://www.buzzfeednews.com/article/skbaer/milkwaukee-bucks-boycott-jacob-blake                               |
| 2020-08-27T13:35:04 | 2020-08-27T17:50:03 |          3 | Hurricane Laura           | https://www.buzzfeednews.com/article/emmanuelfelton/hurricane-laura-could-lead-to-an-environmental-disaster-on |
| 2020-08-27T13:35:04 | 2020-08-27T17:50:03 |          4 | RNC 2020                  | https://www.buzzfeednews.com/article/ryancbrooks/trump-white-house-rnc-backdrop                                |
| 2020-08-27T13:35:04 | 2020-08-27T17:50:03 |          5 | Mike Pence                | https://www.buzzfeednews.com/article/salvadorhernandez/pence-dhs-officer-death-rnc-speech                      |


## Timestamps of all fetches

The [`data/all-timestamps.tsv`](data/all-timestamps.tsv) file contains a simple table of all timestamps for which the script successfully obtained data. If you're using the deduplicated data, this file can provide you with a more precise understanding of the fetch timings within the `timestamp_first` and `timestamp_last` spans.

| timestamp           |
|---------------------|
| 2018-11-13T22:10:02 |
| 2018-11-13T22:15:02 |
| 2018-11-13T22:20:02 |
| 2018-11-13T22:25:02 |
| 2018-11-13T22:30:02 |
| 2018-11-13T22:35:02 |

## Licensing

The data files in this repository are available under Creative Commons’ [CC BY-SA 4.0 license terms](https://creativecommons.org/licenses/by-sa/4.0/). The [code files](scripts/) in this repository are available under the [MIT License terms](https://opensource.org/license/mit/). 
