# SECTION 0: Setup and Variables ----

# Make sure these packages are installed
import pandas as pd
import requests
import json

API_KEY = ""
API_URL = "http://6f7528e6-1c61-4971-bbc6-919eb2810e92.southcentralus.azurecontainer.io/score"


# SECTION 1: API Request Function ----

def inference_request(DayOfWeek, Origin, Dest, DepTimeBlk, ArrTimeBlk, CRSElapsedTime, Distance, DistanceGroup):
  
  # Bind columns to dataframe
  request_df = pd.DataFrame({"DayOfWeek":DayOfWeek, "Origin":Origin, "Dest":Dest, "DepTimeBlk":DepTimeBlk, "ArrTimeBlk":ArrTimeBlk, "CRSElapsedTime":CRSElapsedTime, "Distance":Distance, "DistanceGroup":DistanceGroup})
  
  req = {
      "Inputs": {
          "data": list(request_df.to_dict('records'))
          },
         "GlobalParameters": 0.0
         }
        
  # POST request - send JSON to API
  headers = {'Authorization': ('Bearer ' + API_KEY), 
             'Content-Type': 'application/json'}

  req = str.encode(json.dumps(req))

  result = requests.post(API_URL, data = req, headers=headers)
  return(result)


# SECTION 2: Data preprocessing ----
# Fetch data from Power Query workflow
df = dataset

# Create subset of dataframe that holds distinct flight information for prediction
df_inference = df[['DayOfWeek', 'Origin', 'Dest', 'DepTimeBlk', 'ArrTimeBlk', 'CRSElapsedTime', 'Distance', 'DistanceGroup']].drop_duplicates().reset_index(drop = True)


# SECTION 3: Get Predictions ----
result = inference_request(df_inference['DayOfWeek'], df_inference['Origin'], df_inference['Dest'], df_inference['DepTimeBlk'], df_inference['ArrTimeBlk'], df_inference['CRSElapsedTime'], df_inference['Distance'], df_inference['DistanceGroup'])


# SECTION 4: Data postprocessing ----
result = pd.DataFrame(json.loads(result.content))
df_inference['ELAPSED_TIME_PREDICTED'] = result

# Bring results back to original dataframe
df = df.merge(df_inference, on = ["DayOfWeek", "Origin", "Dest", "DepTimeBlk", "ArrTimeBlk", "CRSElapsedTime", "Distance", "DistanceGroup"], how = 'left')


# SECTION 5: Format output for Power BI ----
output = pd.DataFrame(df.copy())
del df
del df_inference




