# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Loading dataset into Pandas DataFrame
events_df = pd.read_csv('events.csv')
schedules_df = pd.read_csv('schedules.csv')
torch_route_df = pd.read_csv('torch_route.csv')
venues_df = pd.read_csv('venues.csv')

# Inspecting the first few rows of each DataFrame
print("Events DataFrame:")
print(events_df.head())

print("\nSchedules DataFrame:")
print(schedules_df.head())

print("\nTorch Route DataFrame:")
print(torch_route_df.head())

print("\nVenues DataFrame:")
print(venues_df.head())

# Step 2: Explore and Clean Data

# Basic info for each DataFrame
print(events_df.info())
print(events_df.describe())

print(schedules_df.info())
print(schedules_df.describe())

print(torch_route_df.info())
print(torch_route_df.describe())

print(venues_df.info())
print(venues_df.describe())

# Check for missing values
print(events_df.isnull().sum())
print(schedules_df.isnull().sum())
print(torch_route_df.isnull().sum())
print(venues_df.isnull().sum())

# Drop rows with missing values
events_df = events_df.dropna()
schedules_df = schedules_df.dropna()
torch_route_df = torch_route_df.dropna()
venues_df = venues_df.dropna()

# Inspecting the 'venue_code' column in schedules_df
print("Schedules DataFrame 'venue_code' Column:")
print(schedules_df['venue_code'])

# Check for missing values
print("\nMissing values in 'venue_code' column of Schedules DataFrame:")
print(schedules_df['venue_code'].isnull().sum())

# If there are missing values or empty strings, count them
missing_or_empty_venue_codes = schedules_df['venue_code'].isnull().sum() + (schedules_df['venue_code'] == '').sum()
print("\nTotal missing or empty venue codes:", missing_or_empty_venue_codes)

# Print rows with missing or empty 'venue_code' values
print("\nRows with missing or empty 'venue_code':")
print(schedules_df[schedules_df['venue_code'].isnull() | (schedules_df['venue_code'] == '')])

# Fill missing 'venue_code' with 'venue_code_other' if it exists
if 'venue_code_other' in schedules_df.columns:
    schedules_df['venue_code'] = schedules_df['venue_code'].replace('', np.nan).fillna(schedules_df['venue_code_other'])
    print("\nFilled 'venue_code' column with 'venue_code_other' values where necessary")

# Remove rows with empty or missing 'venue_code' values after fill
schedules_df = schedules_df[schedules_df['venue_code'].notnull() & (schedules_df['venue_code'] != '')]

# Check the filled 'venue_code' column
print("Schedules DataFrame 'venue_code' Column after filling:")
print(schedules_df['venue_code'])

# Merge DataFrames on the venue code
merged_df = pd.merge(schedules_df, venues_df, left_on='venue_code', right_on='tag')

# Check the merged DataFrame


#Hypothesis 1: Events held in certain venues attract more participants

# Analyze the number of events held at each venue without merging
venue_event_counts = schedules_df['venue_code'].value_counts().reset_index()
venue_event_counts.columns = ['venue_code', 'event_count']



# Analyze the number of events held at each venue
venue_event_counts = merged_df['venue_code'].value_counts().reset_index()
venue_event_counts.columns = ['venue_code', 'event_count']

print("\nEvent Counts by Venue:")
print(venue_event_counts)

# Visualize the data
plt.figure(figsize=(10, 6))
plt.bar(venue_event_counts['venue_code'], venue_event_counts['event_count'])
plt.xlabel('Venue Code')
plt.ylabel('Number of Events')
plt.title('Number of Events by Venue')
plt.xticks(rotation=90)
plt.tight_layout()  # Ensure everything fits without overlap
plt.show()
