import duckdb

def get_all_data():
    connection = duckdb.connect('fitbit.ddb')

    queries = [
        ('dailyActivity_merged', 
         "SELECT Id AS user_id, ActivityDate, TotalSteps, TotalDistance, "
         "TrackerDistance, LoggedActivitiesDistance, VeryActiveDistance, "
         "ModeratelyActiveDistance, LightActiveDistance, SedentaryActiveDistance, "
         "VeryActiveMinutes, FairlyActiveMinutes, LightlyActiveMinutes, "
         "SedentaryMinutes, Calories FROM dailyActivity_merged"),
        
        ('dailyCalories_merged', 
         "SELECT Id AS user_id, ActivityDay, Calories FROM dailyCalories_merged"),
        
        ('dailyIntensities_merged', 
         "SELECT Id AS user_id, ActivityDay, SedentaryMinutes, LightlyActiveMinutes, "
         "FairlyActiveMinutes, VeryActiveMinutes, SedentaryActiveDistance, "
         "LightActiveDistance, ModeratelyActiveDistance, VeryActiveDistance "
         "FROM dailyIntensities_merged"),
        
        ('dailySteps_merged', 
         "SELECT Id AS user_id, ActivityDay, StepTotal FROM dailySteps_merged"),
        
        ('heartrate_seconds_merged', 
         "SELECT Id AS user_id, Time, Value FROM heartrate_seconds_merged"),
        
        ('hourlyCalories_merged', 
         "SELECT Id AS user_id, ActivityHour, Calories FROM hourlyCalories_merged"),
        
        ('hourlyIntensities_merged', 
         "SELECT Id AS user_id, ActivityHour, TotalIntensity, AverageIntensity "
         "FROM hourlyIntensities_merged"),
        
        ('hourlySteps_merged', 
         "SELECT Id AS user_id, ActivityHour, StepTotal FROM hourlySteps_merged"),
        
        ('minuteCaloriesNarrow_merged', 
         "SELECT Id AS user_id, ActivityMinute, Calories FROM minuteCaloriesNarrow_merged"),
        
        ('minuteCaloriesWide_merged', 
         "SELECT Id AS user_id, ActivityHour, "
         "Calories00, Calories01, Calories02, Calories03, Calories04, "
         "Calories05, Calories06, Calories07, Calories08, Calories09, "
         "Calories10, Calories11, Calories12, Calories13, Calories14, "
         "Calories15, Calories16, Calories17, Calories18, Calories19, "
         "Calories20, Calories21, Calories22, Calories23, Calories24, "
         "Calories25, Calories26, Calories27, Calories28, Calories29, "
         "Calories30, Calories31, Calories32, Calories33, Calories34, "
         "Calories35, Calories36, Calories37, Calories38, Calories39, "
         "Calories40, Calories41, Calories42, Calories43, Calories44, "
         "Calories45, Calories46, Calories47, Calories48, Calories49, "
         "Calories50, Calories51, Calories52, Calories53, Calories54, "
         "Calories55, Calories56, Calories57, Calories58, Calories59 "
         "FROM minuteCaloriesWide_merged"),
        
        ('minuteIntensitiesNarrow_merged', 
         "SELECT Id AS user_id, ActivityMinute, Intensity FROM minuteIntensitiesNarrow_merged"),
        
        ('minuteIntensitiesWide_merged', 
         "SELECT Id AS user_id, ActivityHour, "
         "Intensity00, Intensity01, Intensity02, Intensity03, Intensity04, "
         "Intensity05, Intensity06, Intensity07, Intensity08, Intensity09, "
         "Intensity10, Intensity11, Intensity12, Intensity13, Intensity14, "
         "Intensity15, Intensity16, Intensity17, Intensity18, Intensity19, "
         "Intensity20, Intensity21, Intensity22, Intensity23, Intensity24, "
         "Intensity25, Intensity26, Intensity27, Intensity28, Intensity29, "
         "Intensity30, Intensity31, Intensity32, Intensity33, Intensity34, "
         "Intensity35, Intensity36, Intensity37, Intensity38, Intensity39, "
         "Intensity40, Intensity41, Intensity42, Intensity43, Intensity44, "
         "Intensity45, Intensity46, Intensity47, Intensity48, Intensity49, "
         "Intensity50, Intensity51, Intensity52, Intensity53, Intensity54, "
         "Intensity55, Intensity56, Intensity57, Intensity58, Intensity59 "
         "FROM minuteIntensitiesWide_merged"),
        
        ('minuteMETsNarrow_merged', 
         "SELECT Id AS user_id, ActivityMinute, METs FROM minuteMETsNarrow_merged"),
        
        ('minuteSleep_merged', 
         "SELECT Id AS user_id, date, value, logId FROM minuteSleep_merged"),
        
        ('minuteStepsNarrow_merged', 
         "SELECT Id AS user_id, ActivityMinute, Steps FROM minuteStepsNarrow_merged"),
        
        ('minuteStepsWide_merged', 
         "SELECT Id AS user_id, ActivityHour, "
         "Steps00, Steps01, Steps02, Steps03, Steps04, Steps05, "
         "Steps06, Steps07, Steps08, Steps09, Steps10, Steps11, "
         "Steps12, Steps13, Steps14, Steps15, Steps16, Steps17, "
         "Steps18, Steps19, Steps20, Steps21, Steps22, Steps23, "
         "Steps24, Steps25, Steps26, Steps27, Steps28, Steps29, "
         "Steps30, Steps31, Steps32, Steps33, Steps34, Steps35, "
         "Steps36, Steps37, Steps38, Steps39, Steps40, Steps41, "
         "Steps42, Steps43, Steps44, Steps45, Steps46, Steps47, "
         "Steps48, Steps49, Steps50, Steps51, Steps52, Steps53, "
         "Steps54, Steps55, Steps56, Steps57, Steps58, Steps59 "
         "FROM minuteStepsWide_merged"),
        
        ('sleepDay_merged', 
         "SELECT Id AS user_id, SleepDay, TotalSleepRecords, "
         "TotalMinutesAsleep, TotalTimeInBed FROM sleepDay_merged"),
        
        ('weightLogInfo_merged', 
         "SELECT Id AS user_id, Date, WeightKg, WeightPounds, "
         "Fat, BMI, IsManualReport, LogId FROM weightLogInfo_merged")
    ]

    all_data = {table: connection.execute(query).fetchdf() for table, query in queries}

    connection.close()

    return all_data

def get_user_averages():
    connection = duckdb.connect('fitbit.ddb')
    query = "SELECT * FROM user_averages"
    result = connection.execute(query)
    column_names = [desc[0] for desc in result.description]
    data = result.fetchall()
    connection.close()
    return column_names, data