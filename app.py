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
    stats = continent_stats_df.columns.to_list()
    response = {
        "Message": "Welcome to the Continent Stats App",
        "Continents Available ":continents,
        "Stats Available ":stats
    }
    return(response)

@app.get("/{cont_name}")
def cont_stats(cont_name : str):
    if(cont_name in continent_stats_df["Continent"].to_list()):
        cont_index = continent_stats_df["Continent"].index[continent_stats_df['Continent'] == cont_name]
        response = continent_stats_df.iloc[cont_index].to_dict("records")
        return (response)        
    else:
        raise HTTPException(status_code=404, detail="Continent not found.")
    
@app.get("/{cont_name}/{stat_name}")
def cont_stat(cont_name : str, stat_name :str):
    if(cont_name in continent_stats_df["Continent"].to_list()) and (stat_name in continent_stats_df.columns.to_list()):
        cont_index = continent_stats_df["Continent"].index[continent_stats_df['Continent'] == cont_name]
        result = continent_stats_df.iloc[cont_index][stat_name].tolist()
        return {f"{cont_name}'s {stat_name}":f"{result[0]}"}
    else:
        raise HTTPException(status_code=404, detail="Continent or Stat not found.")