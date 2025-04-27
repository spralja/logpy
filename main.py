from logpy.controller import ExcelController
LOG_PATH  = '/Users/spralja/Library/CloudStorage/OneDrive-Personal/log'
from pathlib import Path
controller = ExcelController(Path(LOG_PATH))




import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone

def get_weeks_entries(year, week):
    start_of_week = datetime.fromisocalendar(year, week, 1).replace(tzinfo=timezone.utc) 
    end_of_week = start_of_week + timedelta(days=7)
    weeks_entries = controller.get_intersection(start_of_week, end_of_week)
    return weeks_entries

def main():
    year, week = 2025, 7
    entries = get_weeks_entries(year, week)
    
    data = []
    for entry in entries:
        data.append((entry.start_time, entry.end_time, entry.category, entry.description))

    df = pd.DataFrame(data, columns=['start_time', 'end_time', 'category', 'description'])

    # Ensure datetime columns are timezone-aware and converted to UTC first
    df['start_time'] = pd.to_datetime(df['start_time'], utc=True)
    df['end_time'] = pd.to_datetime(df['end_time'], utc=True)
    
    # Convert to CEST (UTC+2) for analysis
    cest = timezone(timedelta(hours=2))
    df['start_time'] = df['start_time'].dt.tz_convert(cest)
    df['end_time'] = df['end_time'].dt.tz_convert(cest)
    
    print(df)
    start_of_week = datetime.fromisocalendar(year, week, 1).replace(tzinfo=timezone.utc).astimezone(cest)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    # Check if the first event starts exactly at the beginning of the week
    first_event_starts_correctly = df['start_time'].min() == start_of_week
    # Check if the last event ends exactly at the end of the week
    last_event_ends_correctly = df['end_time'].max() == end_of_week
    
    print(f"First event starts exactly at beginning of week: {first_event_starts_correctly}")
    print(f"Last event ends exactly at end of week: {last_event_ends_correctly}")
    
    # Calculate duration (get_weeks_entries already truncates properly)
    df['duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 3600
    
    # Group by category and sum the duration
    df_week_grouped = df.groupby('category')['duration'].sum().reset_index()
    
    # Print category values and their sum
    print("Category Durations:")
    print(df_week_grouped.to_string(index=False))
    print(f"Total Hours: {df_week_grouped['duration'].sum():.2f}")
    
    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(df_week_grouped['category'], df_week_grouped['duration'])
    plt.xlabel('Category')
    plt.ylabel('Total Hours')
    plt.title(f'Total Hours per Category - Week {week}, {year} (CEST)')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()

if __name__ == '__main__':
    main()
