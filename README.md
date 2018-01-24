# TitleSearch

small module to search for similar or alternative titles on [BakaUpdates](https://www.mangaupdates.com), [MyAnimeList](https://myanimelist.net) and [TheVisualNovelDatabase](https://vndb.org)


### Installing
This script runs with [Python 3](https://www.python.org).

Download this repository and run the setup.py to install all necessary dependencies

### Dependencies

Required:

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup) - html parser
* [html5lib](https://github.com/html5lib/html5lib-python) - standards-compliant library for parsing and serializing HTML documents and fragments in Python
* [numpy](http://www.numpy.org) - fundamental package for scientific computing with Python
* [requests](https://github.com/requests/requests) - http library


### Usage
You can BakaUpdates only as modules:
```
from titlesearch import get_similar_titles, get_alternative_titles

get_similar_titles(example_title)
get_alternative_titles(title=example_title)
```

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