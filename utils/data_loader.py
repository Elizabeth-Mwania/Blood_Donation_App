import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Load and preprocess the main data files"""
    try:
        # donor_candidates = pd.read_csv('data/data_2019_cleaned.csv')
        # donors = pd.read_csv('data/Donnors_2019.csv')
        donor_candidates = pd.read_csv('data/data_2019_cleaned.csv')
        donors = pd.read_csv('data/Donnors_2019.csv')
        
        # Rename columns
        donor_candidates = standardize_column_names(donor_candidates, 'candidate')
        donors = standardize_column_names(donors, 'donor')
        
        # Convert dates
        donor_candidates = convert_dates(donor_candidates)
        
        # Add derived columns
        donor_candidates = add_derived_columns(donor_candidates)
        
        return donor_candidates, donors
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def standardize_column_names(df, dataset_type):
    """Standardize column names based on dataset type"""
    if dataset_type == 'candidate':
        column_mapping = {
            "Date de remplissage de la fiche": "form_fill_date",
            "Date de naissance": "birth_date",
            "Age": "age",
            "Niveau d'etude": "education_level",
            "Genre": "gender",
            "Taille": "height",
            "Poids": "weight",
            "Date de remplissage de la fiche": "form_fill_date",
            "Date de naissance": "birth_date",
            "Age": "age",
            "Niveau d'etude": "education_level",
            "Genre": "gender",
            "Taille": "height",
            "Poids": "weight",
            "Situation Matrimoniale (SM)": "marital_status",
            "Profession": "profession",
            "Arrondissement de residence": "residence_district",
            "Quartier de Residence": "residence_neighborhood",
            "Nationalite": "nationality",
            "Religion": "religion",
            "A-t-il (elle) deja donne le sang": "has_donated_before",
            "Si oui preciser la date du dernier don.": "last_donation_date",
            "Taux d'hemoglobine": "hemoglobin_level",
            "ELIGIBILITE AU DON.": "eligibility",
            
            # Reasons for ineligibility (temporary)
            "Raison indisponibilite  [Est sous anti-biotherapie  ]": "ineligible_antibiotics",
            "Raison indisponibilite  [Taux d'hemoglobine bas ]": "ineligible_low_hemoglobin",
            "Raison indisponibilite  [date de dernier Don < 3 mois ]": "ineligible_recent_donation",
            "Raison indisponibilite  [IST recente (Exclu VIH, Hbs, Hcv)]": "ineligible_recent_sti",
            "Date de dernieres regles (DDR)": "last_menstrual_date",
            "Raison de l'indisponibilite de la femme [La DDR est mauvais si <14 jour avant le don]": "female_ineligible_menstrual",
            "Raison de l'indisponibilite de la femme [Allaitement ]": "female_ineligible_breastfeeding",
            "Raison de l'indisponibilite de la femme [A accoucher ces 6 derniers mois  ]": "female_ineligible_postpartum",
            "Raison de l'indisponibilite de la femme [Interruption de grossesse  ces 06 derniers mois]": "female_ineligible_miscarriage",
            "Raison de l'indisponibilite de la femme [est enceinte ]": "female_ineligible_pregnant",
            "Autre raisons,  preciser": "other_reasons",
            # "Selectionner \"ok\" pour envoyer": "submission_status",
            
            # Permanent ineligibility reasons
            "Raison de non-eligibilite totale  [Antecedent de transfusion]": "total_ineligible_transfusion_history",
            "Raison de non-eligibilite totale  [Porteur(HIV,hbs,hcv)]": "total_ineligible_hiv_hbs_hcv",
            "Raison de non-eligibilite totale  [Opere]": "total_ineligible_surgery",
            "Raison de non-eligibilite totale  [Drepanocytaire]": "total_ineligible_sickle_cell",
            "Raison de non-eligibilite totale  [Diabetique]": "total_ineligible_diabetes",
            "Raison de non-eligibilite totale  [Hypertendus]": "total_ineligible_hypertension",
            "Raison de non-eligibilite totale  [Asthmatiques]": "total_ineligible_asthma",
            "Raison de non-eligibilite totale  [Cardiaque]": "total_ineligible_heart_disease",
            "Raison de non-eligibilite totale  [Tatoue]": "total_ineligible_tattoo",
            "Raison de non-eligibilite totale  [Scarifie]": "total_ineligible_scarification",
            # "Si autres raison preciser": "other_total_ineligible_reasons"
        }
    elif dataset_type == 'donor':
        column_mapping = {
            "Horodateur": "timestamp",
            "Sexe": "gender",
            "Sexe": "gender",
            "Age": "age",
            "Type de donation": "donation_type",
            "Groupe Sanguin ABO/Rhesus": "blood_group",
            "Phenotype": "phenotype"
        }
    
    return df.rename(columns=column_mapping)

def convert_dates(df):
    """Convert date columns to datetime"""
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def add_derived_columns(df):
    """Add derived columns like eligibility flag"""
    if 'eligibility' in df.columns:
        df['is_eligible'] = df['eligibility'].apply(
            lambda x: 1 if str(x).lower() in ['yes', 'oui', '1', 'true', 'eligible'] else 0
        )
    return df

@st.cache_data
def load_geo_data():
    """Load geographic data"""
    districts = ["Douala I", "Douala II", "Douala III", "Douala IV", "Douala V"]
    coords = [[9.7, 4.05], [9.72, 4.08], [9.74, 4.07], [9.71, 4.03], [9.73, 4.06]]
    return pd.DataFrame({
        'district': districts, 
        'lat': [c[0] for c in coords], 
        'lon': [c[1] for c in coords]
    })