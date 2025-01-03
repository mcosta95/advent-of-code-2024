import json
from statistics import mean
import pandas as pd
from datetime import datetime


def transform_datetime(date_):
    return datetime.utcfromtimestamp(date_).strftime("%Y-%m-%d %H:%M:%S")

def count_stars_days_and_parts(members):

    rows = []
    for _, member_data in members.items():
        completed_days = member_data['completion_day_level']

         # Calculate statistics
        name = member_data["name"]
        total_stars_part_1 = sum(1 for day in completed_days.values() if '1' in day)
        total_stars_part_2 = sum(1 for day in completed_days.values() if '2' in day)
        total_stars = member_data['stars']
        local_score = member_data['local_score']
        last_star = transform_datetime(member_data['last_star_ts'])
        days_completed_both_parts = sum(1 for day in completed_days.values() if '1' in day and '2' in day)
        

            # Create a dictionary for the row
        row = {
            "name": name,
            "total_stars_part_1": total_stars_part_1,
            "total_stars_part_2": total_stars_part_2,
            "total_stars": total_stars,
            "days_completed_both_parts": days_completed_both_parts,
            "local_score": local_score,
            "last_star_ts": last_star
        }
        rows.append(row)
    
    df =  pd.DataFrame(rows)

    return df.sort_values(by="total_stars", ascending=False)


def duration_format(duration_seconds):

    duration_minutes, seconds = divmod(duration_seconds, 60)
    hours, minutes = divmod(duration_minutes, 60)
    duration_str = f"{hours} hour {minutes} min {seconds} sec"
    return duration_str

def time_took_days_and_parts(members):

    final_df = pd.DataFrame()
    for _, member_data in members.items():
        completed_days = member_data['completion_day_level']
        # Calculate statistics
        name = member_data["name"]

        rows_days = []
        for each_day, parts in completed_days.items():            
            start_of_day = datetime(2024, 12, int(each_day), 4, 0).timestamp()
            row_day = {
            "name": name,
            "day": int(each_day),
            "time_part_1": transform_datetime(parts['1']['get_star_ts']) if '1' in parts else None,
            "time_part_2": transform_datetime(parts['2']['get_star_ts']) if '2' in parts else None,
            "duration_1": parts['1']['get_star_ts'] - start_of_day if '1' in parts else None,
            "duration_2": parts['2']['get_star_ts'] - parts['1']['get_star_ts'] if '1' in parts and '2' in parts else None,
            "format_dur_part_1": duration_format(parts['1']['get_star_ts'] - start_of_day) if '1' in parts else "Not done",
            "format_dur_part_2": duration_format(parts['2']['get_star_ts'] - parts['1']['get_star_ts']) if '1' in parts and '2' in parts else "Not done"
            }
            rows_days.append(row_day)
    
        df_member =  pd.DataFrame(rows_days)
        final_df = pd.concat([final_df, df_member])

    return final_df



def load_leaderboard(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_statistics(data):
    members = data['members']
    total_days = 25
    
    # 1. Perform table to fetch statistics
    df_stars_stats = count_stars_days_and_parts(members)
    
    df_time_stats = time_took_days_and_parts(members)

    # 2. The overall number of stars completed
    total_days_part = (total_days*len(df_stars_stats))
    percentage_stars_part1 = round((sum(df_stars_stats["total_stars_part_1"])) / total_days_part * 100)
    percentage_stars_part2 = round((sum(df_stars_stats["total_stars_part_2"])) / total_days_part * 100)
    percentage_overall_stars = round((sum(df_stars_stats["total_stars"])) / (total_days_part*2) * 100)
    percentage_completed_days = round((sum(df_stars_stats["days_completed_both_parts"])) / (total_days_part) * 100)


    # 3. The person that recovered faster, that some days did more than once
    df_time_stats['duration_2'] = pd.to_numeric(df_time_stats['duration_2'], errors='coerce')
    fastest_recovery = df_time_stats.loc[df_time_stats['duration_2'].idxmin()]['name']

    # 4. The average for each day of completed it
    day_completion_times = df_time_stats.groupby('day')['duration_1'].apply(list).to_dict()
    average_completion_times = {day: mean(times) for day, times in day_completion_times.items()}
    fastest_completion_day = min(average_completion_times, key=average_completion_times.get)
    slowest_completion_day = max(average_completion_times, key=average_completion_times.get)
    fastest_completion_time = duration_format(average_completion_times[fastest_completion_day])
    slowest_completion_time = duration_format(average_completion_times[slowest_completion_day])

    # 5. What was the hardest day to perform
    hardest_day = slowest_completion_day

    # 6. The person with the highest global score
    highest_global_score = df_stars_stats[df_stars_stats["local_score"] == df_stars_stats["local_score"].max()].name[0]


    # 7. The total number of stars collected by each person
    total_stars_per_person = {member_id: sum(len(parts) for parts in member_data['completion_day_level'].values()) for member_id, member_data in members.items()}

    # 8. The person who collected the most stars
    most_stars_collected = max(total_stars_per_person.items(), key=lambda x: x[1])[0]

    # 9. The average time taken to complete part 1 and part 2 for each day
    average_time_part1 = {}
    average_time_part2 = {}
    for member_data in members.values():
        for day, parts in member_data['completion_day_level'].items():
            if '1' in parts:
                if day not in average_time_part1:
                    average_time_part1[day] = []
                average_time_part1[day].append(parts['1']['get_star_ts'])
            if '2' in parts:
                if day not in average_time_part2:
                    average_time_part2[day] = []
                average_time_part2[day].append(parts['2']['get_star_ts'])
    average_time_part1 = {day: mean(times) for day, times in average_time_part1.items()}
    average_time_part2 = {day: mean(times) for day, times in average_time_part2.items()}

    # 10. The day with the most stars collected
    stars_per_day = {}
    for member_data in members.values():
        for day, parts in member_data['completion_day_level'].items():
            if day not in stars_per_day:
                stars_per_day[day] = 0
            stars_per_day[day] += len(parts)
    most_stars_day = max(stars_per_day.items(), key=lambda x: x[1])[0]
    
    return {
        "all_days_completed": all_days_completed,
        "percentage_stars_part1": percentage_stars_part1,
        "fastest_recovery": fastest_recovery,
        "average_completion_times": average_completion_times,
        "hardest_day": hardest_day,
        "highest_global_score": highest_global_score,
        "total_stars_per_person": total_stars_per_person,
        "most_stars_collected": most_stars_collected,
        "average_time_part1": average_time_part1,
        "average_time_part2": average_time_part2,
        "most_stars_day": most_stars_day
    }

def main():
    file_path = '/Users/costam8/Documents/advent-of-code-2024/data/leaderboard.json'
    data = load_leaderboard(file_path)
    statistics = extract_statistics(data)
    
    print("Statistics:")
    print(f"1. The person that did everyday and completed all the days: {statistics['all_days_completed']}")
    print(f"2. The overall number of stars completed on part 1: {statistics['percentage_stars_part1']:.2f}%")
    print(f"3. The person that recovered faster: {statistics['fastest_recovery']}")
    print(f"4. The average completion time for each day: {statistics['average_completion_times']}")
    print(f"5. The hardest day to perform: {statistics['hardest_day']}")
    print(f"6. The person with the highest global score: {statistics['highest_global_score']}")
    print(f"7. The total number of stars collected by each person: {statistics['total_stars_per_person']}")
    print(f"8. The person who collected the most stars: {statistics['most_stars_collected']}")
    print(f"9. The average time taken to complete part 1 for each day: {statistics['average_time_part1']}")
    print(f"10. The average time taken to complete part 2 for each day: {statistics['average_time_part2']}")
    print(f"11. The day with the most stars collected: {statistics['most_stars_day']}")

if __name__ == "__main__":
    main()