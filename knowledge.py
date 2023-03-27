import cerebro, query_maker
import pandas as pd

# Build the query
l1 = [ "unsupervised adaptation", "teacher student", "model compression"] # "knowledge distillation", "domain adaptation",
l2 = ["online", "real-time", "edge", "human pose estimation", "hpe", "distributed", "collaborative", "knowledge distillation"]

#print(query)
df = pd.DataFrame(columns = ['Year', 'Title', 'Author','Publication'])
# Ask for the specific query
for l in l1:
    query = query_maker.all_permutations([l],l2)
    results = cerebro.ask(query, from_y=2011, to_y=2024, page_limits=30)
    print("\n\nres:")
    print(results)
    df = pd.concat([df,results],ignore_index=True)
    print(l,"completed.",df.info())
    with open('data/query_knowledge_'+l+".txt", 'w') as f:
        f.write(query)
    results.to_csv("data/results_knowledge_" + l + ".csv",index=False)

# Dump the results
with open('data/query_knowledge_27-03-2023.txt', 'w') as f:
    f.write(query)

results = cerebro.clean_results(df)
results.to_csv("data/results_knowledge_27-03-2023.csv",index=False)
results.to_excel("data/results_knowledge_27-03-2023.xlsx")

# Print the summary
print(results.info())

