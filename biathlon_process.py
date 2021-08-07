# Import libraries
import pandas as pd
import json
import os

# Routes
route = r'route_to_parser_result'
outRoute = r'route_to_export_process_result'

# Process
df = pd.read_excel(route, index_col=None, header=None).drop([0])
df = df[[1, 2]]
df.columns = ['name', 'time']
df['time'] = df['time'].astype(float)
df_races = df.groupby(['name']).count()
df_time = df.groupby(['name']).sum()
df_total = df_time.merge(df_races,left_on = 'name', right_on = 'name')
df_total = df_total.sort_values(["time_y", "time_x"], ascending = (False, True))

# Export results
df_total.to_excel(outRoute)