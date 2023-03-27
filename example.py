import cerebro, query_maker

# Perform the query
l1 = ["human motion", "motion capture", "human pose estimation"]
l2 = ["denoising", "completion", "recovery"]
query = query_maker.all_perumtations(l1,l2)

#print(query)

# Ask for the specific query
results = cerebro.ask(query, from_y=1990, to_y=2024, page_limits=30)

# Dump the results
with open('data/query.txt', 'w') as f:
    f.write(query)
results.to_csv("data/result.csv",index=False)

results = cerebro.clean_results(results)
results.to_csv("data/result_clean.csv",index=False)

# Print the summary
print(results.info())

