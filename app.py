from fastapi import FastAPI, HTTPException
import csv
import pandas as pd

path = "C:/Users/adity/Python and related stuff/Countries API Project/world_population.csv"

df = pd.read_csv(path)
#print(df)

continent_stats_df = df.groupby("Continent")["Population"].agg(
    Country_Count = "count",
    Total_Continent_Population = "sum",
    Average_Country_Population = "mean",
    Max_Population_of_a_Country = "max",
    Min_Population_of_a_Country = "min")

continent_stats_df = continent_stats_df.reset_index().round(2)

app = FastAPI() 

@app.get("/")
def home():
    continents = continent_stats_df["Continent"].to_list()
    return(f"Welcome to the Homepage! Here are the available Continents: {continents}")

@app.get("/{cont_name}")
def cont_stats(cont_name : str):
    if(cont_name in continent_stats_df["Continent"].to_list()):
        cont_index = continent_stats_df["Continent"].index[continent_stats_df['Continent'] == cont_name]
        response = continent_stats_df.iloc[cont_index].to_dict("records")
        return (response)        
    else:
        raise HTTPException(status_code=404, detail="Continent not found.")
    
#@app.get("/countries/{cont_name}/{attribute}", response_model=str)
#def cont_stat