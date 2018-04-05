# TitleSearch

[![Build Status](https://travis-ci.org/DaRealFreak/TitleSearch.svg?branch=master)](https://travis-ci.org/DaRealFreak/TitleSearch)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/DaRealFreak/TitleSearch/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/DaRealFreak/TitleSearch/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/DaRealFreak/TitleSearch/badge.svg?branch=master)](https://coveralls.io/github/DaRealFreak/TitleSearch?branch=master)

small module to search for similar or alternative titles on [BakaUpdates](https://www.mangaupdates.com), [MyAnimeList](https://myanimelist.net) and [TheVisualNovelDatabase](https://vndb.org)


### Installing
This project works with [Python 3](https://www.python.org).

Download this repository and run the setup.py to install all necessary dependencies

### Dependencies

Required:

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup) - html parser
* [html5lib](https://github.com/html5lib/html5lib-python) - standards-compliant library for parsing and serializing HTML documents and fragments in Python
* [numpy](http://www.numpy.org) - fundamental package for scientific computing with Python
* [requests](https://github.com/requests/requests) - http library
* [jellyfish](https://github.com/jamesturk/jellyfish) - python library for doing approximate and phonetic matching of strings


### Usage
You can use TitleSearch only as modules:
```
from titlesearch import get_similar_titles, get_alternative_titles

get_similar_titles(title='example_title')
get_alternative_titles(title='example_title')
```
You can also check a working example in the provided [usage.py](https://github.com/DaRealFreak/TitleSearch/blob/master/usage.py)

## Development
Want to contribute? Great!

I'm always glad hearing about bugs or pull requests.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Thanks

A big thanks to 
- [BakaUpdates](https://www.mangaupdates.com) 
- [MyAnimeList](https://myanimelist.net)
- [TheVisualNovelDatabase](https://vndb.org)

who are maintaining their databases with all the titles.