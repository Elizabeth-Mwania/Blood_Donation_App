# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.compose import ColumnTransformer
# from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA
# from sklearn.metrics import silhouette_score
# from sklearn.pipeline import Pipeline
# import warnings
# warnings.filterwarnings('ignore')
# def render(data):
    
#     # Apply filters
#     df = data['donor_candidates']
#     load_and_preprocess(df)
#     print(df.head())
    

# def load_and_preprocess(df):
#     """Load data and preprocess all specified features"""
#     # print(f"Loading data from {file_path}...")
#     try:
#         # df = data['donor_candidates'], data['filters']
#         # Load data with specified columns
#         # columns = ['Age', 'Genre', 'Situation Matrimoniale (SM)','Religion', 'Profession','Quartier de Residence','Nationalite', 'Niveau detude',
#         #           'Taux dhemoglobine', 'Poids']
#         # df = pd.read_excel(file_path)
#         df = df[df["ELIGIBILITE AU DON."] == "Eligible"].copy()
#         df = df.drop(columns=["ELIGIBILITE AU DON.","Si autres raison preciser","Taille"]) # Drop the eligibility column after filtering
#         print(df.head())
#         # Convert hemoglobin to numeric
#         df["Taux dhemoglobine"] = pd.to_numeric(df["Taux dhemoglobine"], errors='coerce')

#         profession_groups = {
#             "Chaudronnier": "Industrie & BTP", "Soudeur": "Industrie & BTP", "Mecanicien": "Industrie & BTP",
#             "Macon": "Industrie & BTP", "Technicien en metallurgie": "Industrie & BTP", "Technicien genie civil": "Industrie & BTP",
#             "Electrotechnicien": "Industrie & BTP", "Electricien en batiment": "Industrie & BTP", "Peintre": "Industrie & BTP",
#             "Plombier": "Industrie & BTP", "Menuisier": "Industrie & BTP", "Carreleur": "Industrie & BTP",
#             "Decorateur batiment": "Industrie & BTP", "Technicien etancheite": "Industrie & BTP",

#             "Commercant": "Commerce & Entrepreneuriat", "Negociant bois": "Commerce & Entrepreneuriat",
#             "Vendeur": "Commerce & Entrepreneuriat", "Entrepreneur": "Commerce & Entrepreneuriat",
#             "Business man": "Commerce & Entrepreneuriat", "Trader": "Commerce & Entrepreneuriat",
#             "Agent commercial": "Commerce & Entrepreneuriat", "Agent immobilier": "Commerce & Entrepreneuriat",
#             "Restaurateur": "Commerce & Entrepreneuriat", "Magasinier": "Commerce & Entrepreneuriat",

#             "Chauffeur": "Transport & Logistique", "Machiniste": "Transport & Logistique", "Docker": "Transport & Logistique",
#             "Grutier": "Transport & Logistique", "Logisticien": "Transport & Logistique", "Transitaire": "Transport & Logistique",
#             "Agent fret airport": "Transport & Logistique", "Gestionnaire de vols": "Transport & Logistique",
#             "Conducteur": "Transport & Logistique",

#             "Secretaire comptable": "Administration & Gestion", "Comptable": "Administration & Gestion",
#             "Comptable financier": "Administration & Gestion", "Gestionnaire": "Administration & Gestion",
#             "Assistant administratif": "Administration & Gestion", "Auditeur interne": "Administration & Gestion",
#             "Administrateur": "Administration & Gestion", "Charge de clientele": "Administration & Gestion",
#             "Charge de communication": "Administration & Gestion", "Intendant infirmier superieur": "Administration & Gestion",

#             "Informaticien": "Informatique & Telecommunications", "Developpeur en informatique": "Informatique & Telecommunications",
#             "Technicien reseaux telecoms": "Informatique & Telecommunications", "Analyste-programmeur": "Informatique & Telecommunications",
#             "Informaticien de reseau": "Informatique & Telecommunications", "Infographe": "Informatique & Telecommunications",
#             "Content manager": "Informatique & Telecommunications",

#             "Enseignant": "Education & Recherche", "Professeur": "Education & Recherche",
#             "Etudiant": "Education & Recherche", "Eleve": "Education & Recherche", "Stagiaire": "Education & Recherche",
#             "Assistant juridique": "Education & Recherche",

#             "Agent de securite": "Securite & Defense", "Chef de securite": "Securite & Defense",
#             "Gendarme": "Securite & Defense", "Militaire": "Securite & Defense", "Brancardier": "Securite & Defense",

#             "Medecin": "Sante & Social", "Personnel de sante": "Sante & Social",
#             "Technicien de laboratoire": "Sante & Social", "Aide chirurgien": "Sante & Social",
#             "Assistant infirmier": "Sante & Social", "Intendant infirmier superieur": "Sante & Social",

#             "Beat maker": "Art & Culture", "Realisateur": "Art & Culture",
#             "Chantre musicien": "Art & Culture", "Serigraphe": "Art & Culture", "Coiffeur": "Art & Culture",

#             "Agent d'entretien": "Services & Autres", "Agent technique": "Services & Autres",
#             "Technicien": "Services & Autres", "Electricien": "Services & Autres", "Hotelier": "Services & Autres",
#             "Patissier": "Services & Autres", "Agent de maintenance industrielle": "Services & Autres",
#             "Employe": "Services & Autres", "Operateur economique": "Services & Autres",

#             "Sans emploi": "Sans emploi & Divers", "Pas precise": "Sans emploi & Divers"
#         }
#         # Map profession to groups
#         df["Profession"] = df["Profession"].map(profession_groups).fillna("Autres")
        
#         # Health-aware weight imputation
#         def impute_weight(row):
#             if pd.isna(row['Poids']):
#                 base_weight = np.random.randint(50, 86)
#                 if pd.notna(row['Taux dhemoglobine']):
#                     hemoglobin = row['Taux dhemoglobine']
#                     if hemoglobin < 12:  # Anemia - likely lower weight
#                         return max(50, base_weight - np.random.randint(0, 5))
#                     elif hemoglobin > 14:  # Higher hemoglobin - possibly more muscular
#                         return min(85, base_weight + np.random.randint(0, 5))
#                 return base_weight
#             return row['Poids']
        
#         df['Poids'] = df.apply(impute_weight, axis=1)
        
#         # Fill remaining missing values
#         for col in df.columns:
#             if df[col].isnull().sum() > 0:
#                 if df[col].dtype in ['int64', 'float64']:
#                     df[col] = df[col].fillna(df[col].median())
#                 else:
#                     df[col] = df[col].fillna(df[col].mode()[0])
        
#         print(f"Data shape after preprocessing: {df.shape}")
#         return df
#     except Exception as e:
#         print(f"Error loading data: {e}")
#         return None



# def prepare_for_clustering(df):
#     """Prepare mixed-type data for clustering"""
#     # Define numeric and categorical features
#     numeric_features = ['Age', 'Taux dhemoglobine', 'Poids']
#     categorical_features = ['Genre', 'Situation Matrimoniale (SM)','Religion', 'Profession','Quartier de Residence', 'Nationalite', 'Niveau detude']
    
#     # Create preprocessing pipeline
#     preprocessor = ColumnTransformer(
#         transformers=[
#             ('num', StandardScaler(), numeric_features),
#             ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
#         ])
    
#     # Apply preprocessing
#     processed_data = preprocessor.fit_transform(df)
    
#     # Get feature names after one-hot encoding
#     cat_encoder = preprocessor.named_transformers_['cat']
#     cat_features = cat_encoder.get_feature_names_out(categorical_features)
#     all_features = numeric_features + list(cat_features)
    
#     return processed_data, all_features

# def find_optimal_clusters(data):
#     """Find optimal number of clusters using elbow method and silhouette score"""
#     max_k = min(10, data.shape[0] // 2)
#     k_range = range(2, max_k + 1)
    
#     inertia = []
#     silhouette_scores = []
    
#     for k in k_range:
#         kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
#         kmeans.fit(data)
#         inertia.append(kmeans.inertia_)
        
#         if data.shape[0] > k + 1:
#             silhouette_avg = silhouette_score(data, kmeans.labels_)
#             silhouette_scores.append(silhouette_avg)
#         else:
#             silhouette_scores.append(0)
    
#     # Plot results
#     plt.figure(figsize=(12, 5))
#     plt.subplot(1, 2, 1)
#     plt.plot(k_range, inertia, 'bo-')
#     plt.xlabel('Number of Clusters')
#     plt.ylabel('Inertia')
#     plt.title('Elbow Method')
    
#     plt.subplot(1, 2, 2)
#     plt.plot(k_range, silhouette_scores, 'ro-')
#     plt.xlabel('Number of Clusters')
#     plt.ylabel('Silhouette Score')
#     plt.title('Silhouette Method')
    
#     plt.tight_layout()
#     plt.savefig('optimal_clusters.png')
#     plt.close()
    
#     optimal_k = k_range[np.argmax(silhouette_scores)] if max(silhouette_scores) > 0 else 3
#     print(f"Optimal number of clusters: {optimal_k}")
    
#     return optimal_k

# def load_and_preprocess(data=None, file_path=None):
#     """Load and preprocess data from either a DataFrame or file path
    
#     Args:
#         data: Dictionary containing 'donor_candidates' DataFrame (optional)
#         file_path: Path to Excel file (optional if data is provided)
    
#     Returns:
#         Preprocessed DataFrame or None if error occurs
#     """
#     try:
#         # Handle input data
#         if data is not None:
#             # Check if data contains the expected structure
#             if isinstance(data, dict) and 'donor_candidates' in data:
#                 print("Loading data from provided dictionary")
#                 df = data['donor_candidates'].copy()
#             else:
#                 print("Using provided DataFrame directly")
#                 df = data.copy()
#         elif file_path is not None:
#             print(f"Loading data from file: {file_path}")
#             df = pd.read_excel(file_path)
#         else:
#             raise ValueError("Either data or file_path must be provided")
        
#         # Debug: Show columns before processing
#         print("Columns in raw data:", df.columns.tolist())
        
#         # Filter for eligible donors if column exists
#         if "ELIGIBILITE AU DON." in df.columns:
#             df = df[df["ELIGIBILITE AU DON."] == "Eligible"].copy()
#             df = df.drop(columns=["ELIGIBILITE AU DON."])
        
#         # Drop specified columns if they exist
#         columns_to_drop = ["Si autres raison preciser", "Taille"]
#         for col in columns_to_drop:
#             if col in df.columns:
#                 df = df.drop(columns=[col])
        
#         # Convert hemoglobin to numeric if column exists
#         if "Taux dhemoglobine" in df.columns:
#             df["Taux dhemoglobine"] = pd.to_numeric(df["Taux dhemoglobine"], errors='coerce')
        
#         # Profession grouping if column exists
#         profession_groups = {
#             "Chaudronnier": "Industrie & BTP",
#             # ... (keep all your existing profession groups)
#             "Pas precise": "Sans emploi & Divers"
#         }
        
#         if "Profession" in df.columns:
#             df["Profession"] = df["Profession"].map(profession_groups).fillna("Autres")
        
#         # Health-aware weight imputation if columns exist
#         if 'Poids' in df.columns and 'Taux dhemoglobine' in df.columns:
#             def impute_weight(row):
#                 if pd.isna(row['Poids']):
#                     base_weight = np.random.randint(50, 86)
#                     if pd.notna(row['Taux dhemoglobine']):
#                         hemoglobin = row['Taux dhemoglobine']
#                         if hemoglobin < 12:
#                             return max(50, base_weight - np.random.randint(0, 5))
#                         elif hemoglobin > 14:
#                             return min(85, base_weight + np.random.randint(0, 5))
#                     return base_weight
#                 return row['Poids']
            
#             df['Poids'] = df.apply(impute_weight, axis=1)
        
#         # Fill remaining missing values
#         for col in df.columns:
#             if df[col].isnull().sum() > 0:
#                 if pd.api.types.is_numeric_dtype(df[col]):
#                     df[col] = df[col].fillna(df[col].median())
#                 else:
#                     df[col] = df[col].fillna(df[col].mode()[0])
        
#         print(f"Data shape after preprocessing: {df.shape}")
#         print("Columns after preprocessing:", df.columns.tolist())
#         return df
        
#     except Exception as e:
#         print(f"Error in load_and_preprocess: {e}")
#         return None

# def perform_clustering(df, data, optimal_k, feature_names):
#     """Perform clustering and analyze results"""
#     # Perform K-means clustering
#     kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
#     cluster_labels = kmeans.fit_predict(data)
#     df['Cluster'] = cluster_labels
    
#     # Reduce dimensions for visualization
#     pca = PCA(n_components=2)
#     reduced_data = pca.fit_transform(data.toarray() if hasattr(data, 'toarray') else data)
    
#     # Plot clusters in 2D PCA space
#     plt.figure(figsize=(10, 8))
#     scatter = plt.scatter(reduced_data[:, 0], reduced_data[:, 1], 
#                          c=cluster_labels, cmap='viridis', alpha=0.7)
#     plt.xlabel('Principal Component 1')
#     plt.ylabel('Principal Component 2')
#     plt.title('Cluster Visualization (PCA-reduced)')
#     plt.colorbar(scatter, label='Cluster')
#     plt.savefig('cluster_visualization.png')
#     plt.close()
    
#     # Analyze cluster characteristics
#     print("\n--- Cluster Sizes ---")
#     print(df['Cluster'].value_counts().sort_index())
    
#     # Calculate mean values for numeric features by cluster
#     numeric_features = ['Age', 'Taux dhemoglobine', 'Poids']
#     if len(numeric_features) > 0:
#         print("\n--- Numeric Feature Averages by Cluster ---")
#         print(df.groupby('Cluster')[numeric_features].mean())
    
#     # Calculate mode for categorical features by cluster
#     categorical_features = ['Genre', 'Situation Matrimoniale (SM)','Religion', 'Profession','Quartier de Residence','Nationalite', 'Niveau detude']
#     for cat in categorical_features:
#         print(f"\n--- Most common {cat} by Cluster ---")
#         print(df.groupby('Cluster')[cat].agg(lambda x: x.mode()[0]))
    
#     return cluster_labels

# def run_clustering_pipeline(file_path):
#     """Full clustering pipeline from raw data to results"""
#     df = load_and_preprocess(file_path)
#     if df is None:
#         return None
    
#     processed_data, feature_names = prepare_for_clustering(df)
#     optimal_k = find_optimal_clusters(processed_data)
#     cluster_labels = perform_clustering(df, processed_data, optimal_k, feature_names)
    
#     # Add cluster labels to original data
#     df['Cluster'] = cluster_labels
#     return df

# def get_cluster_profiles(df):
#     """Generate summary statistics for each cluster"""
#     profiles = {}
    
#     # Numeric features summary
#     numeric_features = ['Age', 'Taux dhemoglobine', 'Poids']
#     numeric_summary = df.groupby('Cluster')[numeric_features].mean()
    
#     # Categorical features summary
#     categorical_features = ['Genre', 'Situation Matrimoniale (SM)', 'Religion', 
#                            'Profession', 'Quartier de Residence', 'Nationalite', 
#                            'Niveau detude']
    
#     categorical_summary = {}
#     for feature in categorical_features:
#         categorical_summary[feature] = df.groupby('Cluster')[feature].agg(lambda x: x.mode()[0])
    
#     profiles['numeric'] = numeric_summary
#     profiles['categorical'] = categorical_summary
#     profiles['sizes'] = df['Cluster'].value_counts().sort_index()
    
#     return profiles

# def main():
#     """Main clustering workflow"""
#     # Load and preprocess data
#     df = load_and_preprocess('data/data_2019_cleaned.xlsx')
#     if df is None:
#         return
    
#     # Prepare data for clustering
#     processed_data, feature_names = prepare_for_clustering(df)
    
#     # Find optimal clusters
#     optimal_k = find_optimal_clusters(processed_data)
    
#     # Perform clustering
#     cluster_labels = perform_clustering(df, processed_data, optimal_k, feature_names)
    
#     # Save results
#     df.to_excel('clustered_data.xlsx', index=False)
#     print("\nClustering complete. Results saved to 'clustered_data.xlsx'")

# if __name__ == "__main__":
#     main()

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA
# from sklearn.metrics import silhouette_score
# import warnings
# warnings.filterwarnings('ignore')

# # 1. Load the data
# def load_data(file_path,usecols=None):
# # def load_data(file_path):
#     """Load data from Excel file"""
#     print(f"Loading data from {file_path}...")
#     # Read Excel file into a pandas DataFrame
#     try:
#         # df = pd.read_excel(file_path)
#         # df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=usecols)
#         columns_to_load = ['Age', 'Genre', 'Situation Matrimoniale (SM)', 'Profession','Arrondissement de residence', 
#                            'Nationalite', 'Niveau detude','Taux dhemoglobine', 'Poids']
#         # df = load_data('final_3.xlsx', sheet_name='2019_Cleaned', usecols=columns_to_load)
#         df = pd.read_excel(file_path,usecols=columns_to_load)
#         df["Taux dhemoglobine"] = pd.to_numeric(df["Taux dhemoglobine"], errors='coerce')
#         print(f"Successfully loaded data with shape: {df.shape}")
#         return df
#     except Exception as e:
#         print(f"Error loading data: {e}")
#         return None

# # 2. Explore and preprocess the data
# def explore_and_preprocess(df):
#     """Explore and preprocess the data"""
#     # Display basic information
#     print("\n--- Data Overview ---")
#     print(f"Number of records: {df.shape[0]}")
#     print(f"Number of features: {df.shape[1]}")
    
#     # Display column types
#     print("\n--- Column Data Types ---")
#     print(df.dtypes)
    
#     # Check for missing values
#     missing_values = df.isnull().sum()
#     print("\n--- Missing Values ---")
#     print(missing_values[missing_values > 0] if missing_values.sum() > 0 else "No missing values")
    
#     # Convert datetime columns to numeric features (days since minimum date)
#     datetime_cols = df.select_dtypes(include=['datetime64']).columns
#     for col in datetime_cols:
#         if not df[col].isnull().all():  # Skip if all values are null
#             # Convert to days since minimum date
#             min_date = df[col].min()
#             df[f'{col}_days'] = (df[col] - min_date).dt.days
#             print(f"Converted {col} to {col}_days (days since {min_date})")
    
#     # Fill missing values or drop rows as appropriate
#     # For numerical columns, fill with median

#     numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
#     for col in numeric_cols:
#         if df[col].isnull().sum() > 0:
#             df[col] = df[col].fillna(df[col].median())
    
#     # For categorical columns, fill with mode
#     categorical_cols = df.select_dtypes(include=['object']).columns
#     for col in categorical_cols:
#         if df[col].isnull().sum() > 0:
#             df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
#             # df = pd.get_dummies(df, drop_first=True)
    
#     # Drop any remaining rows with missing values
#     original_rows = df.shape[0]
#     df = df.dropna()
#     if df.shape[0] < original_rows:
#         print(f"Dropped {original_rows - df.shape[0]} rows with missing values")
    
#     # Convert categorical variables to numeric using one-hot encoding
#     # Exclude datetime columns to avoid issues
#     non_datetime_cols = [col for col in df.columns if col not in datetime_cols]
#     try:
#         df_encoded = pd.get_dummies(df[non_datetime_cols], drop_first=True)
#         # Add the converted datetime columns back
#         for col in datetime_cols:
#             date_col = f'{col}_days'
#             if date_col in df.columns:
#                 df_encoded[date_col] = df[date_col]
#     except Exception as e:
#         print(f"Error during one-hot encoding: {e}")
#         print("Falling back to numeric features only")
#         df_encoded = df.select_dtypes(include=['int64', 'float64'])
    
#     print(f"\nData shape after preprocessing: {df_encoded.shape}")
#     print(df_encoded.head())
#     return df_encoded, df

# # # 3. Feature selection for clustering
# # def select_features(df_encoded):
# #     """Select relevant features for clustering"""
# #     # # Identify demographic and health-related features
    
# #     # # Common demographic features might include:
# #     # # demographic_patterns = ['Age', 'Genre', 'Situation Matrimoniale (SM)', 'Profession','Arrondissement de residence', 
# #     # #                        'Nationalite', 'Niveau detude']
    
# #     # # # Common health-related features might include:
# #     # # health_patterns = ['Taux dhemoglobine', 'Poids']
    
# #     # # Find columns that match these patterns
# #     # selected_cols = ['Age', 'Genre', 'Situation Matrimoniale (SM)', 'Profession','Arrondissement de residence', 
# #     #                        'Nationalite', 'Niveau detude','Taux dhemoglobine', 'Poids']
    
# #     # for col in df_encoded.columns:
# #     #     col_lower = col.lower()
# #     #     if any(pattern in col_lower for pattern in demographic_patterns + health_patterns):
# #     #         selected_cols.append(col)
    
# #     # if len(selected_cols) == 0:
# #     #     print("No matching demographic or health features found. Using all numeric features instead.")
# #     #     selected_cols = df_encoded.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
# #     # print(f"\nSelected {len(selected_cols)} features for clustering:")
# #     # print(", ".join(selected_cols[:10]) + ("..." if len(selected_cols) > 10 else ""))

# #     numeric_cols = df_encoded.select_dtypes(include=['int64', 'float64']).columns.tolist()
# #     categorical_cols = df_encoded.select_dtypes(include=['object', 'category']).columns.tolist()
    
# #     return df_encoded[numeric_cols + categorical_cols]

# # 4. Determine optimal number of clusters
# def find_optimal_clusters(features_df):
#     """Find the optimal number of clusters using the elbow method and silhouette score"""
#     # Handle the case where there are too few samples
#     if features_df.shape[0] < 10:
#         print("Warning: Few samples for clustering. Using 2 clusters.")
#         # Still need to scale the features
#         scaler = StandardScaler()
#         features_scaled = scaler.fit_transform(features_df)
#         return 2, features_scaled
    
#     # Apply standardization to scale the features
#     scaler = StandardScaler()
#     features_scaled = scaler.fit_transform(features_df)
    
#     # Determine range for k based on dataset size
#     max_k = min(10, features_df.shape[0] // 2)
#     min_k = min(2, max_k)
#     if max_k <= min_k:
#         print(f"Warning: Limited dataset size. Using {min_k} clusters.")
#         return min_k, features_scaled
    
#     k_range = range(min_k, max_k + 1)
    
#     # Calculate inertia (within-cluster sum of squares) for different k values
#     inertia = []
#     silhouette_scores = []
    
#     for k in k_range:
#         print(f"Testing with {k} clusters...")
#         try:
#             kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
#             kmeans.fit(features_scaled)
#             inertia.append(kmeans.inertia_)
            
#             # Calculate silhouette score if we have enough samples
#             if features_df.shape[0] > k + 1:
#                 silhouette_avg = silhouette_score(features_scaled, kmeans.labels_)
#                 silhouette_scores.append(silhouette_avg)
#                 print(f"Silhouette score for {k} clusters: {silhouette_avg:.4f}")
#             else:
#                 silhouette_scores.append(0)
#                 print(f"Not enough samples for silhouette score with {k} clusters")
#         except Exception as e:
#             print(f"Error with {k} clusters: {e}")
#             inertia.append(float('inf'))
#             silhouette_scores.append(0)
    
#     # Plot the elbow curve if we have multiple k values
#     if len(k_range) > 1:
#         plt.figure(figsize=(12, 5))
        
#         plt.subplot(1, 2, 1)
#         plt.plot(k_range, inertia, 'bo-')
#         plt.xlabel('Number of Clusters')
#         plt.ylabel('Inertia')
#         plt.title('Elbow Method for Optimal k')
#         plt.grid(True)
        
#         plt.subplot(1, 2, 2)
#         plt.plot(k_range, silhouette_scores, 'ro-')
#         plt.xlabel('Number of Clusters')
#         plt.ylabel('Silhouette Score')
#         plt.title('Silhouette Method for Optimal k')
#         plt.grid(True)
        
#         plt.tight_layout()
#         plt.savefig('optimal_clusters.png')
    
#     # Find the optimal k based on the silhouette score or elbow method
#     if silhouette_scores and max(silhouette_scores) > 0:
#         optimal_k = k_range[silhouette_scores.index(max(silhouette_scores))]
#     else:
#         # Simple elbow method - find the "elbow" point
#         optimal_k = k_range[0]  # Default to minimum k
        
#         # If we have enough data points for elbow detection
#         if len(inertia) > 2:
#             # Calculate the angle for each point in the curve
#             angles = []
#             for i in range(1, len(inertia) - 1):
#                 x1, y1 = i-1, inertia[i-1]
#                 x2, y2 = i, inertia[i]
#                 x3, y3 = i+1, inertia[i+1]
                
#                 # Calculate vectors
#                 v1 = [x2-x1, y2-y1]
#                 v2 = [x3-x2, y3-y2]
                
#                 # Normalize vectors
#                 v1_norm = (v1[0]**2 + v1[1]**2)**0.5
#                 v2_norm = (v2[0]**2 + v2[1]**2)**0.5
                
#                 if v1_norm * v2_norm == 0:
#                     angles.append(0)
#                 else:
#                     # Calculate angle
#                     dot_product = v1[0]*v2[0] + v1[1]*v2[1]
#                     cos_angle = dot_product / (v1_norm * v2_norm)
#                     cos_angle = max(min(cos_angle, 1.0), -1.0)  # Ensure in valid range
#                     angle = np.arccos(cos_angle)
#                     angles.append(angle)
            
#             if angles:
#                 optimal_k = k_range[angles.index(max(angles)) + 1]
    
#     print(f"\nOptimal number of clusters based on analysis: {optimal_k}")
#     return optimal_k, features_scaled

# # 5. Perform K-means clustering
# def perform_kmeans(features_scaled, optimal_k):
#     """Perform K-means clustering with the optimal number of clusters"""
#     kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
#     cluster_labels = kmeans.fit_predict(features_scaled)
    
#     # Visualize the clusters using PCA
#     pca = PCA(n_components=2)
#     features_pca = pca.fit_transform(features_scaled)
    
#     plt.figure(figsize=(10, 8))
#     scatter = plt.scatter(features_pca[:, 0], features_pca[:, 1], c=cluster_labels, 
#                          cmap='viridis', alpha=0.8, edgecolor='k', s=80)
#     plt.colorbar(scatter, label='Cluster')
#     plt.xlabel('Principal Component 1')
#     plt.ylabel('Principal Component 2')
#     plt.title(f'Donor Clusters Visualization (k={optimal_k})')
#     plt.grid(True, alpha=0.3)
#     plt.savefig('donor_clusters.png')
    
#     return cluster_labels, kmeans.cluster_centers_

# # 6. Analyze cluster profiles
# def analyze_clusters(df, features_df, cluster_labels, cluster_centers, optimal_k):
#     """Analyze and profile the clusters"""
#     # Add cluster labels to the original dataframe
#     df['Cluster'] = cluster_labels
    
#     # Calculate cluster sizes
#     cluster_sizes = df['Cluster'].value_counts().sort_index()
#     print("\n--- Cluster Sizes ---")
#     for cluster, size in cluster_sizes.items():
#         print(f"Cluster {cluster}: {size} donors ({size/len(df)*100:.1f}%)")
    
#     # Profile each cluster by calculating mean values for key features
#     print("\n--- Cluster Profiles ---")
#     # Only include numeric columns when calculating means to avoid datetime errors
#     numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
#     # Make sure 'Cluster' is included for groupby
#     if 'Cluster' not in numeric_cols and 'Cluster' in df.columns:
#         numeric_cols.append('Cluster')
    
#     cluster_profiles = df[numeric_cols].groupby('Cluster').mean()
    
#     # Select a subset of important features for display
#     profile_features = features_df.columns[:10]  # Adjust based on your data
    
#     # For each cluster, identify the top distinguishing features
#     for cluster in range(optimal_k):
#         print(f"\nCluster {cluster} Profile:")
        
#         # Only use numeric features to avoid datetime issues
#         numeric_features = features_df.select_dtypes(include=['int64', 'float64'])
        
#         # Compare this cluster's means to the overall means
#         overall_means = numeric_features.mean()
#         cluster_means = numeric_features[df['Cluster'] == cluster].mean()
        
#         # Calculate the difference as a percentage, avoiding division by zero
#         diff_pct = pd.Series(index=overall_means.index)
#         for feature in overall_means.index:
#             if overall_means[feature] != 0:
#                 diff_pct[feature] = ((cluster_means[feature] - overall_means[feature]) / overall_means[feature] * 100)
#             else:
#                 diff_pct[feature] = 0
#         diff_pct = diff_pct.fillna(0)
        
#         # Sort by absolute difference to find distinguishing features
#         distinguishing_features = diff_pct.abs().sort_values(ascending=False).index[:5]
        
#         for feature in distinguishing_features:
#             if feature in overall_means:
#                 avg_value = overall_means[feature]
#                 cluster_value = cluster_means[feature]
#                 diff = diff_pct[feature]
                
#                 direction = "higher" if diff > 0 else "lower"
#                 print(f"- {feature}: {cluster_value:.2f} ({abs(diff):.1f}% {direction} than average of {avg_value:.2f})")
    
#     # Visualize the distribution of each cluster for a key feature (example: age if available)
#     key_features = []
#     # Only consider numeric features for visualization
#     numeric_features = features_df.select_dtypes(include=['int64', 'float64']).columns
    
#     for pattern in ['age', 'income', 'frequency', 'amount', 'total']:
#         matching_cols = [col for col in numeric_features if pattern in col.lower()]
#         if matching_cols:
#             key_features.extend(matching_cols[:2])  # Take at most 2 features per pattern
    
#     # If no specific features found, use the first two numeric features
#     if not key_features and len(numeric_features) > 0:
#         key_features = numeric_features[:2]
    
#     if key_features:
#         for feature in key_features[:2]:  # Plot first two key features
#             try:
#                 plt.figure(figsize=(12, 6))
#                 for cluster in range(optimal_k):
#                     subset = df[df['Cluster'] == cluster]
#                     if len(subset) > 1:  # Need at least 2 points for KDE plot
#                         sns.kdeplot(subset[feature], label=f'Cluster {cluster}')
#                     else:
#                         plt.axvline(x=subset[feature].iloc[0], color=f'C{cluster}', 
#                                    linestyle='--', label=f'Cluster {cluster}')
                
#                 plt.xlabel(feature)
#                 plt.ylabel('Density')
#                 plt.title(f'Distribution of {feature} Across Clusters')
#                 plt.legend()
#                 plt.grid(True, alpha=0.3)
#                 plt.savefig(f'{feature}_distribution.png')
#             except Exception as e:
#                 print(f"Could not create distribution plot for {feature}: {e}")
    
#     return cluster_profiles

# # 7. Name the clusters and provide recommendations
# def name_clusters(cluster_profiles, df):
#     """Assign meaningful names to clusters and provide actionable recommendations"""
    
#     # Placeholder for cluster names and recommendations
#     cluster_names = {}
#     recommendations = {}
    
#     # Example logic (modify based on your actual data)
#     for cluster in cluster_profiles.index:
#         # Create placeholder names and recommendations
#         cluster_names[cluster] = f"Donor Segment {cluster+1}"
#         recommendations[cluster] = [
#             f"Personalized engagement strategy for {cluster_names[cluster]}",
#             "Tailor communication frequency and channel",
#             "Develop specific appeal messaging"
#         ]
    
#     print("\n--- Donor Segments and Recommendations ---")
#     for cluster, name in cluster_names.items():
#         print(f"\n{name} (Cluster {cluster}):")
#         print("Recommendations:")
#         for rec in recommendations[cluster]:
#             print(f"- {rec}")
    
#     return cluster_names, recommendations

# # 8. Main function to run the analysis
# def main():
#     """Main function to run the donor clustering analysis"""
#     file_path = 'final_3.xlsx'
    
#     # Load the data
#     df = load_data(file_path)
#     if df is None:
#         return
    
#     # Explore and preprocess the data
#     df_encoded, original_df = explore_and_preprocess(df)
    
#     # Select features for clustering
#     features_df = df_encoded
    
#     # Find the optimal number of clusters
#     optimal_k, features_scaled = find_optimal_clusters(features_df)
    
#     # Perform K-means clustering
#     cluster_labels, cluster_centers = perform_kmeans(features_scaled, optimal_k)
    
#     # Analyze cluster profiles
#     cluster_profiles = analyze_clusters(original_df, features_df, cluster_labels, cluster_centers, optimal_k)
    
#     # Name the clusters and provide recommendations
#     cluster_names, recommendations = name_clusters(cluster_profiles, original_df)
    
#     print("\nDonor profiling analysis complete. Results saved as PNG files.")

# if __name__ == "__main__":
#     main()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')


# 1. Load and preprocess data with all features
def load_and_preprocess(file_path):
    """Load data and preprocess all specified features"""
    print(f"Loading data from {file_path}...")
    try:
        # Load data with specified columns
        columns = ['Age', 'Genre', 'Situation Matrimoniale (SM)','Religion', 'Profession','Quartier de Residence','Nationalite', 'Niveau d\'etude',
                  'Taux d\'hemoglobine', 'Poids']
        df = pd.read_excel(file_path,usecols=['ELIGIBILITE AU DON.'] + columns)
        df = df[df["ELIGIBILITE AU DON."] == "Eligible"].copy()
        df = df.drop(columns=["ELIGIBILITE AU DON."]) # Drop the eligibility column after filtering
         
        # Convert hemoglobin to numeric
        df["Taux d\'hemoglobine"] = pd.to_numeric(df["Taux d\'hemoglobine"], errors='coerce')

        profession_groups = {
            "Chaudronnier": "Industrie & BTP", "Soudeur": "Industrie & BTP", "Mecanicien": "Industrie & BTP",
            "Macon": "Industrie & BTP", "Technicien en metallurgie": "Industrie & BTP", "Technicien genie civil": "Industrie & BTP",
            "Electrotechnicien": "Industrie & BTP", "Electricien en batiment": "Industrie & BTP", "Peintre": "Industrie & BTP",
            "Plombier": "Industrie & BTP", "Menuisier": "Industrie & BTP", "Carreleur": "Industrie & BTP",
            "Decorateur batiment": "Industrie & BTP", "Technicien etancheite": "Industrie & BTP",

            "Commercant": "Commerce & Entrepreneuriat", "Negociant bois": "Commerce & Entrepreneuriat",
            "Vendeur": "Commerce & Entrepreneuriat", "Entrepreneur": "Commerce & Entrepreneuriat",
            "Business man": "Commerce & Entrepreneuriat", "Trader": "Commerce & Entrepreneuriat",
            "Agent commercial": "Commerce & Entrepreneuriat", "Agent immobilier": "Commerce & Entrepreneuriat",
            "Restaurateur": "Commerce & Entrepreneuriat", "Magasinier": "Commerce & Entrepreneuriat",

            "Chauffeur": "Transport & Logistique", "Machiniste": "Transport & Logistique", "Docker": "Transport & Logistique",
            "Grutier": "Transport & Logistique", "Logisticien": "Transport & Logistique", "Transitaire": "Transport & Logistique",
            "Agent fret airport": "Transport & Logistique", "Gestionnaire de vols": "Transport & Logistique",
            "Conducteur": "Transport & Logistique",

            "Secretaire comptable": "Administration & Gestion", "Comptable": "Administration & Gestion",
            "Comptable financier": "Administration & Gestion", "Gestionnaire": "Administration & Gestion",
            "Assistant administratif": "Administration & Gestion", "Auditeur interne": "Administration & Gestion",
            "Administrateur": "Administration & Gestion", "Charge de clientele": "Administration & Gestion",
            "Charge de communication": "Administration & Gestion", "Intendant infirmier superieur": "Administration & Gestion",

            "Informaticien": "Informatique & Telecommunications", "Developpeur en informatique": "Informatique & Telecommunications",
            "Technicien reseaux telecoms": "Informatique & Telecommunications", "Analyste-programmeur": "Informatique & Telecommunications",
            "Informaticien de reseau": "Informatique & Telecommunications", "Infographe": "Informatique & Telecommunications",
            "Content manager": "Informatique & Telecommunications",

            "Enseignant": "Education & Recherche", "Professeur": "Education & Recherche",
            "Etudiant": "Education & Recherche", "Eleve": "Education & Recherche", "Stagiaire": "Education & Recherche",
            "Assistant juridique": "Education & Recherche",

            "Agent de securite": "Securite & Defense", "Chef de securite": "Securite & Defense",
            "Gendarme": "Securite & Defense", "Militaire": "Securite & Defense", "Brancardier": "Securite & Defense",

            "Medecin": "Sante & Social", "Personnel de sante": "Sante & Social",
            "Technicien de laboratoire": "Sante & Social", "Aide chirurgien": "Sante & Social",
            "Assistant infirmier": "Sante & Social", "Intendant infirmier superieur": "Sante & Social",

            "Beat maker": "Art & Culture", "Realisateur": "Art & Culture",
            "Chantre musicien": "Art & Culture", "Serigraphe": "Art & Culture", "Coiffeur": "Art & Culture",

            "Agent d'entretien": "Services & Autres", "Agent technique": "Services & Autres",
            "Technicien": "Services & Autres", "Electricien": "Services & Autres", "Hotelier": "Services & Autres",
            "Patissier": "Services & Autres", "Agent de maintenance industrielle": "Services & Autres",
            "Employe": "Services & Autres", "Operateur economique": "Services & Autres",

            "Sans emploi": "Sans emploi & Divers", "Pas precise": "Sans emploi & Divers"
        }
        # Map profession to groups
        df["Profession"] = df["Profession"].map(profession_groups).fillna("Autres")
        
        # Health-aware weight imputation
        def impute_weight(row):
            if pd.isna(row['Poids']):
                base_weight = np.random.randint(50, 86)
                if pd.notna(row['Taux d\'hemoglobine']):
                    hemoglobin = row['Taux d\'hemoglobine']
                    if hemoglobin < 12:  # Anemia - likely lower weight
                        return max(50, base_weight - np.random.randint(0, 5))
                    elif hemoglobin > 14:  # Higher hemoglobin - possibly more muscular
                        return min(85, base_weight + np.random.randint(0, 5))
                return base_weight
            return row['Poids']
        
        df['Poids'] = df.apply(impute_weight, axis=1)
        
        # Fill remaining missing values
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype in ['int64', 'float64']:
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
        
        print(f"Data shape after preprocessing: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# 2. Prepare data for clustering with mixed types
def prepare_for_clustering(df):
    """Prepare mixed-type data for clustering"""
    # Define numeric and categorical features
    numeric_features = ['Age', 'Taux d\'hemoglobine', 'Poids']
    categorical_features = ['Genre', 'Situation Matrimoniale (SM)','Religion', 'Profession','Quartier de Residence', 'Nationalite', 'Niveau d\'etude']
    
    # Create preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # Apply preprocessing
    processed_data = preprocessor.fit_transform(df)
    
    # Get feature names after one-hot encoding
    cat_encoder = preprocessor.named_transformers_['cat']
    cat_features = cat_encoder.get_feature_names_out(categorical_features)
    all_features = numeric_features + list(cat_features)
    
    return processed_data, all_features

# 3. Determine optimal number of clusters
def find_optimal_clusters(data):
    """Find optimal number of clusters using elbow method and silhouette score"""
    max_k = min(10, data.shape[0] // 2)
    k_range = range(2, max_k + 1)
    
    inertia = []
    silhouette_scores = []
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(data)
        inertia.append(kmeans.inertia_)
        
        if data.shape[0] > k + 1:
            silhouette_avg = silhouette_score(data, kmeans.labels_)
            silhouette_scores.append(silhouette_avg)
        else:
            silhouette_scores.append(0)
    
    # Plot results
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(k_range, inertia, 'bo-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method')
    
    plt.subplot(1, 2, 2)
    plt.plot(k_range, silhouette_scores, 'ro-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Method')
    
    plt.tight_layout()
    plt.savefig('optimal_clusters.png')
    plt.close()
    
    optimal_k = k_range[np.argmax(silhouette_scores)] if max(silhouette_scores) > 0 else 3
    print(f"Optimal number of clusters: {optimal_k}")
    
    return optimal_k

# 4. Perform clustering and analyze results
def perform_clustering(df, data, optimal_k, feature_names):
    """Perform clustering and analyze results"""
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(data)
    df['Cluster'] = cluster_labels
    
    # Reduce dimensions for visualization
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data.toarray() if hasattr(data, 'toarray') else data)
    
    # Plot clusters in 2D PCA space
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(reduced_data[:, 0], reduced_data[:, 1], 
                         c=cluster_labels, cmap='viridis', alpha=0.7)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('Cluster Visualization (PCA-reduced)')
    plt.colorbar(scatter, label='Cluster')
    plt.savefig('../assets/images/cluster_visualization.png')
    plt.close()
    
    # Analyze cluster characteristics
    print("\n--- Cluster Sizes ---")
    print(df['Cluster'].value_counts().sort_index())
    
    # Calculate mean values for numeric features by cluster
    numeric_features = ['Age', 'Taux d\'hemoglobine', 'Poids']
    if len(numeric_features) > 0:
        print("\n--- Numeric Feature Averages by Cluster ---")
        print(df.groupby('Cluster')[numeric_features].mean())
    
    # Calculate mode for categorical features by cluster
    categorical_features = ['Genre', 'Situation Matrimoniale (SM)','Religion', 'Profession','Quartier de Residence','Nationalite', 'Niveau d\'etude']
    for cat in categorical_features:
        print(f"\n--- Most common {cat} by Cluster ---")
        print(df.groupby('Cluster')[cat].agg(lambda x: x.mode()[0]))
    
    return cluster_labels

def main():
    """Main clustering workflow"""
    # Load and preprocess data
    df = load_and_preprocess('../data/data_2019_cleaned.xlsx')
    if df is None:
        return
    
    # Prepare data for clustering
    processed_data, feature_names = prepare_for_clustering(df)
    
    # Find optimal clusters
    optimal_k = find_optimal_clusters(processed_data)
    
    # Perform clustering
    cluster_labels = perform_clustering(df, processed_data, optimal_k, feature_names)
    
    # Save results
    df.to_excel('../data/clustered_data.xlsx', index=False)
    print("\nClustering complete. Results saved to '../data/clustered_data.xlsx'")

if __name__ == "__main__":
    main()