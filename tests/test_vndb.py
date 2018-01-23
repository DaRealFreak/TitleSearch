from titlesearch.vndb import VisualNovelDatabase

example_title = "Kantai Collection"

print('similar titles for: "{0:s}"'.format(example_title))
results = VisualNovelDatabase.get_similar_titles(example_title)
for title in results:
    print('similarity: {1:.2f}%, title: "{0:s}"'.format(title['title'], float(title['similarity']) * 100))

print('')
print('alternative titles for: "{0:s}"'.format(example_title))
alternate_titles = VisualNovelDatabase.get_alternative_titles(title=example_title)
for language in alternate_titles:
    for title in alternate_titles[language]:
        print("[{0:s}]: {1:s}".format(language, title))