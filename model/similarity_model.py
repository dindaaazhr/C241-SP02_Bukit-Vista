import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances

class SimilarityModel:
    def __init__(self, pipeline, clust_df, num_cols, cat_cols, priority_factor=2):
        self.pipeline = pipeline
        self.clust_df = clust_df
        self.num_cols = num_cols
        self.cat_cols = cat_cols
        self.priority_factor = priority_factor

    def get_similar_units(self, unit_id):
        clust_df = self.clust_df
        pipeline = self.pipeline
        num_cols = self.num_cols
        cat_cols = self.cat_cols
        priority_factor = self.priority_factor

        # Retrieve data with the given unit_id
        input_data = clust_df[clust_df['unit_id'] == unit_id]
        if input_data.empty:
            print(f"No data found for unit_id {unit_id}.")
            return None

        # Fit the preprocessor on the entire dataset
        pipeline.named_steps['preprocessor'].fit(clust_df[num_cols + cat_cols])

        # Filter the DataFrame to only include rows from the same cluster as the input
        input_cluster = input_data['cluster_label'].values[0]
        filtered_clust_df = clust_df[clust_df['cluster_label'] == input_cluster]

        # If there are no units in the same cluster, fallback to the entire dataset
        if filtered_clust_df.empty:
            filtered_clust_df = clust_df.copy()

        # Reset the index of filtered_clust_df
        filtered_clust_df = filtered_clust_df.reset_index(drop=True)

        # Apply the preprocessor to the filtered dataset
        X_transformed = pipeline.named_steps['preprocessor'].transform(filtered_clust_df[num_cols + cat_cols])

        # Retrieve the transformed feature names
        num_features = num_cols
        cat_features = pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(cat_cols)
        all_features = np.concatenate([num_features, cat_features])

        # Identify the index of the 'avg_price_per_day' column
        price_col_index = np.where(all_features == 'avg_price_per_day')[0][0]

        # Identify the indices of the 'area_regency_city' columns (one-hot encoded)
        area_cols_indices = [i for i, col in enumerate(all_features) if col.startswith('area_regency_city')]

        # Apply the priority factor to the priority columns
        X_transformed[:, price_col_index] *= priority_factor
        X_transformed[:, area_cols_indices] *= priority_factor

        # Extract the features from the input data
        input_features = input_data[num_cols + cat_cols]

        # Apply the preprocessor to the input features
        input_transformed = pipeline.named_steps['preprocessor'].transform(input_features)

        # Apply the priority factor to the priority columns in the input data
        input_transformed[:, price_col_index] *= priority_factor
        input_transformed[:, area_cols_indices] *= priority_factor

        # Calculate the distance between the input data and each data in the same cluster using Euclidean distance
        distances = euclidean_distances(input_transformed, X_transformed)

        # Filter data by the same area_regency_city
        input_area_regency_city = input_data['area_regency_city'].values[0]
        same_area_indices = filtered_clust_df[filtered_clust_df['area_regency_city'] == input_area_regency_city].index

        # Define input_property_id before the if statement
        input_property_id = input_data['property_id'].values[0]

        # If there are units in the same area_regency_city, prioritize them
        if len(same_area_indices) > 1:
            # Filter distances to only consider units in the same area_regency_city
            same_area_distances = {index: distances[0, index] for index in same_area_indices if filtered_clust_df.iloc[index]['property_id'] != input_property_id}
            # Sort distances within the same area_regency_city
            sorted_indices = sorted(same_area_distances, key=same_area_distances.get)[:3]
        else:
            # If no units are in the same area_regency_city, fallback to the entire dataset
            sorted_distances = np.argsort(distances[0])
            # Filter out data that has the same property_id as the input
            filtered_indices = [index for index in sorted_distances if filtered_clust_df.iloc[index]['property_id'] != input_property_id]
            # Select the 3 nearest qualifying data points
            sorted_indices = filtered_indices[:3]

        # Return the 3 nearest data points
        closest_data = filtered_clust_df.iloc[sorted_indices]

        # If closest_data is still empty, calculate distances for the entire dataset and return the 3 nearest units
        if closest_data.empty:
            X_transformed_all = pipeline.named_steps['preprocessor'].transform(clust_df[num_cols + cat_cols])
            distances_all = euclidean_distances(input_transformed, X_transformed_all)
            sorted_distances_all = np.argsort(distances_all[0])
            filtered_indices_all = [index for index in sorted_distances_all if clust_df.iloc[index]['property_id'] != input_property_id]
            sorted_indices_all = filtered_indices_all[:3]
            closest_data = clust_df.iloc[sorted_indices_all]

        input_data = clust_df[clust_df['unit_id'] == unit_id]

        combined_data = pd.concat([closest_data, input_data], ignore_index=True)
        return combined_data