import pandas as pd

# Read the CSV files into DataFrames
updated_skin_df = pd.read_csv("updated_skin.csv")
cosmetic_p_df = pd.read_csv("Products/cosmetic_p.csv")

# Drop the specified columns from cosmetic_p_df
cosmetic_p_df = cosmetic_p_df.drop(columns=["Sensitive", "ingredients"])

# Sort cosmetic_p_df by rank in descending order
sorted_cosmetic_p_df = cosmetic_p_df.sort_values(by="rank", ascending=False)

# Print unique labels in cosmetic_p_df for debugging
print("Unique Labels in cosmetic_p_df:")
print(cosmetic_p_df["Label"].unique())

# Initialize an empty DataFrame to store the results
results_df = pd.DataFrame(columns=["name", "rank", "label"])

# Iterate through each row in updated_skin_df
for _, row in updated_skin_df.iterrows():
    labels = [label.strip('"') for label in row["Label"].split(", ")]  # Remove quotes
    combination = row["Combination"]
    dry = row["Dry"]
    normal = row["Normal"]
    oily = row["Oily"]

    # Iterate through each label
    for label in labels:
        print("Processing label:", label)

        # Filter cosmetic_p_df based on label and skin type
        filtered_cosmetic_df = sorted_cosmetic_p_df[
            (sorted_cosmetic_p_df["Label"].str.strip('"') == label)
            & (
                (sorted_cosmetic_p_df["Combination"] == combination)
                | (sorted_cosmetic_p_df["Dry"] == dry)
                | (sorted_cosmetic_p_df["Normal"] == normal)
                | (sorted_cosmetic_p_df["Oily"] == oily)
            )
        ]

        # If there are matching products, add them to the results
        if not filtered_cosmetic_df.empty:
            result_rows = filtered_cosmetic_df[["name", "rank"]].assign(label=label)
            results_df = pd.concat([results_df, result_rows])

# Display the results
print(results_df)

# If you want to save it to a new CSV file:
# results_df.to_csv('path/to/results.csv', index=False)
