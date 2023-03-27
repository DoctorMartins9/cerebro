# cerebro
Search from Google Scholar effectively

# Usage

Build the query
```
l1 = ["human motion", "motion capture", "human pose estimation"]
l2 = ["denoising", "completion", "recovery"]
query = query_maker.all_perumtations(l1,l2)
```

Ask to cerebro:
```
results = cerebro.ask(query, from_y=1990, to_y=2024, page_limits=30)
```

Clean the results:
```
results = cerebro.clean_results(results)
```

And then you can dump the results.

# References

- [Scraping Google Scholar](https://medium.com/@nandinisaini021/scraping-publications-of-aerial-image-research-papers-on-google-scholar-using-python-a0dee9744728)
- [Detecting Chinese Characters ](https://medium.com/the-artificial-impostor/detecting-chinese-characters-in-unicode-strings-4ac839ba313a)
