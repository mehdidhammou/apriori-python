import pandas as pd

# Read the original transactional CSV file
df = pd.read_csv("Market_Basket_Optimisation.csv", header=None)

# Binarize the transactions
binarized_df = (
    pd.get_dummies(df.stack(), prefix="", prefix_sep="").groupby(level=0).max()
)

# Convert True and False to t and ''
binarized_df = binarized_df.replace({True: 1, False: 0})

# Save to CSV file
binarized_df.to_csv("transactions_binarized.csv", index=False, header=True)

print("Binarized CSV file created successfully!")
