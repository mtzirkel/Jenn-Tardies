import pandas as pd

years = ['15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22']
dfs = []
for year in years:
    df = pd.read_excel(f'IC_Downloads/{year}_BHS_att.xlsx')
    columns_map = {'student_studentNumber': 'lunch#',
                   'student_grade': 'grade',
                   'attendancePeriodCount_periodName': 'period',
                   'attendancePeriodCount_periodAbsences': 'total_absences',
                   'attendancePeriodCount_absencesExcused': 'excused',
                   'attendancePeriodCount_absencesUnexcused': 'unexcused',
                   'attendancePeriodCount_tardies': 'tardies',
                   'attendancePeriodCount_termName': 'semester',
                   'attendancePeriodCount_scheduleName': 'day_of_week',
                   'attendancePeriodCount_calendarID': 'calendar_id'}
    df = df.rename(columns=columns_map)
    dfs.append(df)
final = pd.concat(dfs, ignore_index=True)

years_cov = {92: '15-16', 126: '16-17', 137: '17-18', 152: '18-19', 175: '19-20', 177: '20-21', 197: '21-22'}

final['calendar_id'] = final['calendar_id'].map(years_cov)
final.to_csv('working_data.csv', index=False)
