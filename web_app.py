from flask import Flask, render_template
import pandas as pd
from datetime import datetime, timedelta, timezone
from logpy.controller import ExcelController
from pathlib import Path
import plotly.express as px
import plotly.utils
import json
import pytz

app = Flask(__name__)

# Initialize the controller
LOG_PATH = '/Users/spralja/Library/CloudStorage/OneDrive-Personal/log'
controller = ExcelController(Path(LOG_PATH))

# Define timezones
CEST = timezone(timedelta(hours=2))
CPH_TZ = pytz.timezone('Europe/Copenhagen')

# Semester dates
SEMESTER_START = datetime(2025, 2, 3, tzinfo=CEST)  # 3rd February 2025
SEMESTER_END = datetime(2025, 5, 12, tzinfo=CEST)   # 12th May 2025

def get_weeks_entries(year, week):
    # Create week start at 00:00 CEST
    start_of_week = datetime.fromisocalendar(year, week, 1).replace(
        hour=0, minute=0, second=0, microsecond=0,
        tzinfo=CEST
    ).astimezone(timezone.utc)
    
    end_of_week = start_of_week + timedelta(days=7)
    weeks_entries = controller.get_intersection(start_of_week, end_of_week)
    return weeks_entries

def prepare_data(year, week):
    entries = get_weeks_entries(year, week)
    
    data = []
    for entry in entries:
        # Convert from UTC to CEST
        start_time = entry.start_time.astimezone(CEST)
        end_time = entry.end_time.astimezone(CEST)
        data.append((start_time, end_time, entry.category, entry.description))

    df = pd.DataFrame(data, columns=['start_time', 'end_time', 'category', 'description'])
    
    # Calculate duration in hours
    df['duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 3600
    
    # Add date and day of week (using CEST dates)
    df['date'] = df['start_time'].dt.date
    df['day_of_week'] = df['start_time'].dt.day_name()
    
    return df

def prepare_semester_data():
    # Get entries from semester start to end
    entries = controller.get_intersection(
        SEMESTER_START.astimezone(timezone.utc),
        SEMESTER_END.astimezone(timezone.utc)
    )
    
    data = []
    course_time = {}  # Track time per course
    meta_time = 0     # Track total meta time (misc + commute)
    
    for entry in entries:
        if entry.category == 'Academic':  # Only include academic entries
            start_time = entry.start_time.astimezone(CEST)
            end_time = entry.end_time.astimezone(CEST)
            duration = (end_time - start_time).total_seconds() / 3600
            
            if duration > 24:  # Skip unusually long entries
                continue
            
            # Truncate course name at first space
            course_name = entry.description.split(' ')[0] if entry.description else 'Unknown'
            
            # Track time for actual courses and meta activities
            if course_name in ['IML', 'PHPC', 'MC']:
                course_time[course_name] = course_time.get(course_name, 0) + duration
                data.append({
                    'date': start_time.date(),
                    'course': course_name,
                    'duration': duration
                })
            elif course_name in ['misc', 'commute']:
                meta_time += duration
    
    if not data:
        return None
        
    # Calculate total course time and proportions
    total_course_time = sum(course_time.values())
    if total_course_time > 0:  # Avoid division by zero
        course_proportions = {course: time/total_course_time for course, time in course_time.items()}
    else:
        course_proportions = {'IML': 1/3, 'PHPC': 1/3, 'MC': 1/3}  # Default equal distribution if no course time
    
    # Distribute meta time proportionally
    for entry in entries:
        if entry.category == 'Academic':
            start_time = entry.start_time.astimezone(CEST)
            course_name = entry.description.split(' ')[0] if entry.description else 'Unknown'
            
            if course_name in ['misc', 'commute']:
                duration = (entry.end_time - entry.start_time).total_seconds() / 3600
                if duration > 24:
                    continue
                    
                # Distribute meta time to each course
                for course, proportion in course_proportions.items():
                    distributed_duration = duration * proportion
                    data.append({
                        'date': start_time.date(),
                        'course': course,
                        'duration': distributed_duration
                    })
    
    df = pd.DataFrame(data)
    
    # Calculate course totals
    course_totals = df.groupby('course')['duration'].sum().reset_index()
    course_totals = course_totals.sort_values('duration', ascending=False)
    
    # Calculate weekly course breakdown using ISO week numbers
    df['week'] = pd.to_datetime(df['date']).dt.isocalendar().week
    weekly_courses = df.groupby(['week', 'course'])['duration'].sum().reset_index()
    
    # Calculate total hours per week
    weekly_totals = df.groupby('week')['duration'].sum().reset_index()
    
    return {
        'course_totals': course_totals,
        'weekly_courses': weekly_courses,
        'weekly_totals': weekly_totals
    }

def prepare_long_term_data(year):
    # Get all weeks in the year
    all_data = []
    for week in range(1, 53):  # ISO weeks can go up to 53
        try:
            # Create week start at 00:00 CEST
            start_of_week = datetime.fromisocalendar(year, week, 1).replace(
                hour=0, minute=0, second=0, microsecond=0,
                tzinfo=CEST
            ).astimezone(timezone.utc)
            
            end_of_week = start_of_week + timedelta(days=7)
            entries = controller.get_intersection(start_of_week, end_of_week)
            
            for entry in entries:
                # Convert to CEST for date calculations
                start_time = entry.start_time.astimezone(CEST)
                end_time = entry.end_time.astimezone(CEST)
                
                # Calculate duration in hours
                duration = (end_time - start_time).total_seconds() / 3600
                
                # Ensure we're not counting the same time twice
                if duration > 24:
                    print(f"Warning: Unusually long duration detected: {duration} hours")
                    print(f"Start: {start_time}, End: {end_time}")
                    continue
                
                all_data.append({
                    'week': week,
                    'date': start_time.date(),
                    'category': entry.category,
                    'duration': duration
                })
        except ValueError:
            # Skip weeks that don't exist
            continue
    
    df = pd.DataFrame(all_data)
    if df.empty:
        return None
    
    # Calculate weekly totals and verify they're reasonable
    weekly_totals = df.groupby('week')['duration'].sum().reset_index()
    for _, row in weekly_totals.iterrows():
        if row['duration'] > 168:  # More than 24*7 hours
            print(f"Warning: Week {row['week']} has {row['duration']} hours")
            # Adjust to maximum possible hours
            weekly_totals.loc[weekly_totals['week'] == row['week'], 'duration'] = 168
    
    # Calculate category distribution per week
    weekly_categories = df.groupby(['week', 'category'])['duration'].sum().reset_index()
    
    # Calculate monthly totals
    df['month'] = pd.to_datetime(df['date']).dt.month
    monthly_totals = df.groupby('month')['duration'].sum().reset_index()
    
    # Calculate monthly category distribution
    monthly_categories = df.groupby(['month', 'category'])['duration'].sum().reset_index()
    
    return {
        'weekly_totals': weekly_totals,
        'weekly_categories': weekly_categories,
        'monthly_totals': monthly_totals,
        'monthly_categories': monthly_categories
    }

@app.route('/')
def index():
    # Get current year and week in CEST
    current_date = datetime.now(CEST)
    year = current_date.isocalendar()[0]
    week = current_date.isocalendar()[1]
    
    df = prepare_data(year, week)
    
    # Create category duration plot
    df_grouped = df.groupby('category')['duration'].sum().reset_index()
    fig_category = px.bar(df_grouped, x='category', y='duration',
                         title=f'Total Hours per Category - Week {week}, {year} (CEST)',
                         labels={'duration': 'Total Hours', 'category': 'Category'})
    category_plot = json.dumps(fig_category, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Create daily breakdown plot
    df_daily = df.groupby(['date', 'category'])['duration'].sum().reset_index()
    fig_daily = px.bar(df_daily, x='date', y='duration', color='category',
                      title=f'Daily Hours by Category - Week {week}, {year} (CEST)',
                      labels={'duration': 'Hours', 'date': 'Date', 'category': 'Category'})
    daily_plot = json.dumps(fig_daily, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Calculate total hours
    total_hours = df['duration'].sum()
    
    # Prepare detailed daily breakdown
    daily_details = []
    for date in sorted(df['date'].unique()):
        day_entries = df[df['date'] == date]
        day_total = day_entries['duration'].sum()
        entries = []
        for _, entry in day_entries.iterrows():
            entries.append({
                'start': entry['start_time'].strftime('%H:%M'),
                'end': entry['end_time'].strftime('%H:%M'),
                'category': entry['category'],
                'duration': f"{entry['duration']:.2f} hours"
            })
        daily_details.append({
            'date': date.strftime('%A, %Y-%m-%d'),
            'total_hours': f"{day_total:.2f}",
            'entries': entries
        })
    
    # Prepare long-term data
    long_term_data = prepare_long_term_data(year)
    if long_term_data:
        # Weekly trends
        fig_weekly = px.line(long_term_data['weekly_totals'], x='week', y='duration',
                           title=f'Weekly Total Hours - {year}',
                           labels={'duration': 'Total Hours', 'week': 'Week Number'})
        weekly_plot = json.dumps(fig_weekly, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Weekly categories
        fig_weekly_cat = px.area(long_term_data['weekly_categories'], x='week', y='duration', color='category',
                                title=f'Weekly Hours by Category - {year}',
                                labels={'duration': 'Hours', 'week': 'Week Number', 'category': 'Category'})
        weekly_cat_plot = json.dumps(fig_weekly_cat, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Monthly trends
        fig_monthly = px.bar(long_term_data['monthly_totals'], x='month', y='duration',
                            title=f'Monthly Total Hours - {year}',
                            labels={'duration': 'Total Hours', 'month': 'Month'})
        monthly_plot = json.dumps(fig_monthly, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Monthly categories
        fig_monthly_cat = px.bar(long_term_data['monthly_categories'], x='month', y='duration', color='category',
                                title=f'Monthly Hours by Category - {year}',
                                labels={'duration': 'Hours', 'month': 'Month', 'category': 'Category'})
        monthly_cat_plot = json.dumps(fig_monthly_cat, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        weekly_plot = None
        weekly_cat_plot = None
        monthly_plot = None
        monthly_cat_plot = None
    
    # Prepare semester data
    semester_data = prepare_semester_data()
    if semester_data:
        # Course totals
        fig_courses = px.bar(semester_data['course_totals'], x='course', y='duration',
                           title='Total Hours per Course (Spring 2024)',
                           labels={'duration': 'Total Hours', 'course': 'Course'})
        courses_plot = json.dumps(fig_courses, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Weekly course breakdown
        fig_weekly_courses = px.area(semester_data['weekly_courses'], x='week', y='duration', color='course',
                                   title='Weekly Hours by Course (Spring 2024)',
                                   labels={'duration': 'Hours', 'week': 'Week Number', 'course': 'Course'})
        weekly_courses_plot = json.dumps(fig_weekly_courses, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Weekly totals
        fig_semester_weekly = px.line(semester_data['weekly_totals'], x='week', y='duration',
                                    title='Weekly Total Hours (Spring 2024)',
                                    labels={'duration': 'Total Hours', 'week': 'Week Number'})
        semester_weekly_plot = json.dumps(fig_semester_weekly, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        courses_plot = None
        weekly_courses_plot = None
        semester_weekly_plot = None
    
    return render_template('index.html',
                         category_plot=category_plot,
                         daily_plot=daily_plot,
                         total_hours=total_hours,
                         year=year,
                         week=week,
                         daily_details=daily_details,
                         weekly_plot=weekly_plot,
                         weekly_cat_plot=weekly_cat_plot,
                         monthly_plot=monthly_plot,
                         monthly_cat_plot=monthly_cat_plot,
                         courses_plot=courses_plot,
                         weekly_courses_plot=weekly_courses_plot,
                         semester_weekly_plot=semester_weekly_plot)

if __name__ == '__main__':
    app.run(debug=True) 