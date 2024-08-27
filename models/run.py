import pandas as pd
import joblib


def load_model(model_filename):
    """Loads a pre-trained model from a file using joblib."""
    model = joblib.load(model_filename)
    return model


def run_model_on_csv(input_csv, model_filename, output_csv, new_column_name='Prediction'):
    """
    Loads a model, applies it to the input CSV, and saves the results to the output CSV.
    
    Parameters:
    - input_csv: Path to the input CSV file.
    - model_filename: Path to the saved model file (e.g., 'model_ai_ml3.pkl').
    - output_csv: Path to save the output CSV file with predictions.
    - new_column_name: Name of the new column that will contain the predictions.
    """
    # Load the model
    model = load_model(model_filename)
    
    # Load the input CSV into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Handle NaN values in 'postContent'
    df['postContent'] = df['postContent'].fillna('')
    
    # Predict using the model on 'postContent'
    df[new_column_name] = model.predict(df['postContent'])
    
    # Save the DataFrame with the predictions to a new CSV file
    df.to_csv(output_csv, index=False)

# Example usage for West Monroe:
#run_model_on_csv('data.csv', 'aiml/model_ai_ml3.pkl', 'aiml.csv', new_column_name='AI/ML')
#run_model_on_csv('aiml.csv', 'customer_centricity/model_cc3.pkl', 'cc.csv', new_column_name='CC')
#run_model_on_csv('cc.csv', 'data_analytics/model_da.pkl', 'da.csv', new_column_name='DA')
#run_model_on_csv('da.csv', 'digital_transformation/model_dt.pkl', 'dt.csv', new_column_name='DT')
#run_model_on_csv('dt.csv', 'hcd/model_hcd3.pkl', 'hcd.csv', new_column_name='HCD')
#run_model_on_csv('hcd.csv', 'innovation/model_i.pkl', 'i.csv', new_column_name='I')
#run_model_on_csv('i.csv', 'ocm/model_ocm3.pkl', 'ocm.csv', new_column_name='OCM')
#run_model_on_csv('ocm.csv', 'product_dev/model_pd.pkl', 'pd.csv', new_column_name='PD')
#run_model_on_csv('pd.csv', 'research_dev/model_rd3.pkl', 'rd.csv', new_column_name='RD')
#run_model_on_csv('rd.csv', 'transactions/model_t3.pkl', 't.csv', new_column_name='T')
#run_model_on_csv('t.csv', 'ux/model_ux.pkl', 'final.csv', new_column_name='UX')

# Example usage for ESP:
#run_model_on_csv('data.csv', 'aiml/model_ai_ml3.pkl', 'aiml.csv', new_column_name='AI/ML')
#run_model_on_csv('aiml.csv', 'cost_management/model_cost_management.pkl', 'cm.csv', new_column_name='CM')
#run_model_on_csv('cm.csv', 'customer_centricity/model_cc3.pkl', 'cx.csv', new_column_name='CX') # This is customer experience, but with the customer centricity model
#run_model_on_csv('cx.csv', 'data_analytics/model_da.pkl', 'da.csv', new_column_name='DA')
#run_model_on_csv('da.csv', 'data_cybersecurity/model_data_cybersecurity.pkl', 'dc.csv', new_column_name='DC')
#run_model_on_csv('dc.csv', 'dei/model_dei.pkl', 'dei.csv', new_column_name='DEI')
#run_model_on_csv('dei.csv', 'economic_outlook/model_economic_outlook2.pkl', 'eo.csv', new_column_name='EO')
#run_model_on_csv('eo.csv', 'environmental/model_environmental.pkl', 'env.csv', new_column_name='Env')
#run_model_on_csv('env.csv', 'geopolitics/model_geopolitics.pkl', 'geo.csv', new_column_name='Geo')
#run_model_on_csv('geo.csv', 'health_insurance/model_health_insurance.pkl', 'hi.csv', new_column_name='HI')
#run_model_on_csv('hi.csv', 'health_outcomes/model_health_outcomes.pkl', 'ho.csv', new_column_name='HO')
#run_model_on_csv('ho.csv', 'product_dev/model_pd.pkl', 'pd.csv', new_column_name='PD')
#run_model_on_csv('pd.csv', 'regulation/model_regulation.pkl', 'reg.csv', new_column_name='Reg')
#run_model_on_csv('reg.csv', 'supply_chain/model_supply_chain.pkl', 'sc.csv', new_column_name='SC')
#run_model_on_csv('sc.csv', 'transactions/model_t3.pkl', 't.csv', new_column_name='T')
#run_model_on_csv('ux.csv', 'workforce_strategy/model_workforce_strat2.pkl', 'final.csv', new_column_name='WS')
