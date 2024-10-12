import csv
import os
import duckdb
from query import get_all_data

def save_user_averages():
    raw_data = get_all_data()
    activity_data = raw_data['dailyActivity_merged']
    sleep_data = raw_data['sleepDay_merged']
    weight_data = raw_data['weightLogInfo_merged']
    heart_rate_data = raw_data['heartrate_seconds_merged']

    heart_rate_averages = {}
    for row in heart_rate_data.itertuples(index=False):
        user_id = row.user_id
        if user_id not in heart_rate_averages:
            heart_rate_averages[user_id] = []
        heart_rate_averages[user_id].append(row.Value)

    for user_id in heart_rate_averages:
        heart_rate_averages[user_id] = round(sum(heart_rate_averages[user_id]) / len(heart_rate_averages[user_id]), 2)

    formatted_data = {}

    for row in activity_data.itertuples(index=False):
        user_id = row.user_id
        
        if user_id not in formatted_data:
            formatted_data[user_id] = {
                'user_id': user_id,
                'total_steps': 0,
                'total_distance': 0.0,
                'calories': 0,
                'very_active_minutes': 0,
                'fairly_active_minutes': 0,
                'lightly_active_minutes': 0,
                'sedentary_minutes': 0,
                'total_minutes_asleep': 'N/A',
                'weight_kg': 'N/A',
                'avg_heart_rate': heart_rate_averages.get(user_id, 'N/A'),
                'days_count': 0,
            }

        data = formatted_data[user_id]
        data['total_steps'] += row.TotalSteps
        data['total_distance'] += round(row.TotalDistance, 2)
        data['calories'] += row.Calories
        data['very_active_minutes'] += row.VeryActiveMinutes
        data['fairly_active_minutes'] += row.FairlyActiveMinutes
        data['lightly_active_minutes'] += row.LightlyActiveMinutes
        data['sedentary_minutes'] += row.SedentaryMinutes
        data['days_count'] += 1

    for user_id, data in formatted_data.items():
        sleep_record = next((s for s in sleep_data.itertuples(index=False) if s.user_id == user_id), None)
        weight_record = next((w for w in weight_data.itertuples(index=False) if w.user_id == user_id), None)
        
        data['total_minutes_asleep'] = sleep_record.TotalMinutesAsleep if sleep_record else 'N/A'
        data['weight_kg'] = round(weight_record.WeightKg, 2) if weight_record else 'N/A'

    for user_id, data in formatted_data.items():
        days_count = data['days_count']
        if days_count > 0:
            data.update({
                'avg_steps': round(data['total_steps'] / days_count, 2),
                'avg_distance': round(data['total_distance'] / days_count, 2),
                'avg_calories': round(data['calories'] / days_count, 2),
                'avg_very_active_minutes': round(data['very_active_minutes'] / days_count, 2),
                'avg_fairly_active_minutes': round(data['fairly_active_minutes'] / days_count, 2),
                'avg_lightly_active_minutes': round(data['lightly_active_minutes'] / days_count, 2),
                'avg_sedentary_minutes': round(data['sedentary_minutes'] / days_count, 2),
                'avg_minutes_asleep': round(data['total_minutes_asleep'], 2) if isinstance(data['total_minutes_asleep'], (int, float)) else 'N/A'
            })

    save_to_csv(formatted_data)
    save_to_db(formatted_data)

def save_to_csv(formatted_data):
    csv_file = "user_averages.csv"
    
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'user_id', 'avg_steps', 'avg_distance', 'avg_calories',
                'avg_minutes_asleep', 'avg_very_active_minutes',
                'avg_fairly_active_minutes', 'avg_lightly_active_minutes',
                'avg_sedentary_minutes', 'weight_kg', 'avg_heart_rate'
            ])
            writer.writeheader()
            for user_data in formatted_data.values():
                writer.writerow({
                    'user_id': user_data['user_id'],
                    'avg_steps': user_data.get('avg_steps', 'N/A'),
                    'avg_distance': user_data.get('avg_distance', 'N/A'),
                    'avg_calories': user_data.get('avg_calories', 'N/A'),
                    'avg_minutes_asleep': user_data.get('avg_minutes_asleep', 'N/A'),
                    'avg_very_active_minutes': user_data.get('avg_very_active_minutes', 'N/A'),
                    'avg_fairly_active_minutes': user_data.get('avg_fairly_active_minutes', 'N/A'),
                    'avg_lightly_active_minutes': user_data.get('avg_lightly_active_minutes', 'N/A'),
                    'avg_sedentary_minutes': user_data.get('avg_sedentary_minutes', 'N/A'),
                    'weight_kg': user_data.get('weight_kg', 'N/A'),
                    'avg_heart_rate': user_data.get('avg_heart_rate', 'N/A'),
                })

def save_to_db(formatted_data):
    conn = duckdb.connect('fitbit.ddb')
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_averages (
        user_id BIGINT,
        avg_steps FLOAT,
        avg_distance FLOAT,
        avg_calories FLOAT,
        avg_minutes_asleep FLOAT,
        avg_very_active_minutes FLOAT,
        avg_fairly_active_minutes FLOAT,
        avg_lightly_active_minutes FLOAT,
        avg_sedentary_minutes FLOAT,
        weight_kg FLOAT,
        avg_heart_rate FLOAT
    )
    """
    conn.execute(create_table_query)

    insert_query = """
    INSERT INTO user_averages (user_id, avg_steps, avg_distance, avg_calories, avg_minutes_asleep,
                                avg_very_active_minutes, avg_fairly_active_minutes,
                                avg_lightly_active_minutes, avg_sedentary_minutes,
                                weight_kg, avg_heart_rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    for user_data in formatted_data.values():
        conn.execute(insert_query, (
            user_data['user_id'],
            user_data.get('avg_steps') if user_data.get('avg_steps') != 'N/A' else None,
            user_data.get('avg_distance') if user_data.get('avg_distance') != 'N/A' else None,
            user_data.get('avg_calories') if user_data.get('avg_calories') != 'N/A' else None,
            user_data.get('avg_minutes_asleep') if user_data.get('avg_minutes_asleep') != 'N/A' else None,
            user_data.get('avg_very_active_minutes') if user_data.get('avg_very_active_minutes') != 'N/A' else None,
            user_data.get('avg_fairly_active_minutes') if user_data.get('avg_fairly_active_minutes') != 'N/A' else None,
            user_data.get('avg_lightly_active_minutes') if user_data.get('avg_lightly_active_minutes') != 'N/A' else None,
            user_data.get('avg_sedentary_minutes') if user_data.get('avg_sedentary_minutes') != 'N/A' else None,
            user_data.get('weight_kg') if user_data.get('weight_kg') != 'N/A' else None,
            user_data.get('avg_heart_rate') if user_data.get('avg_heart_rate') != 'N/A' else None,
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    save_user_averages()
