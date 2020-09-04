import csv
from datetime import datetime


'''

    Opening Input/Output CSV files
    
'''
file_input = open('youtube_data/USvideos.csv', 'r', encoding="Latin1")
file_output = open('youtube_data/output.csv', 'w', encoding="Latin1")
reader = csv.DictReader(file_input)

fieldnames = ['video_id', 'trending_date', 'publish_date', 'title', 'channel_title', 'category_id', 'num_days_trending', 'days_till_trending']
writer = csv.DictWriter(file_output, fieldnames= fieldnames, lineterminator = '\n')
writer.writeheader()
first_row = next(reader) # Ignore Header Files



'''

    String-Date format helper functions

'''
def format_trending_date(str):
    return datetime.strptime(str, '%y.%d.%m')
def format_publish_date(str):
    return datetime.strptime(str.split("T")[0], '%Y-%m-%d')




'''

    group all rows with same video_id into one single row with the attributes in "video_stats" dictionary

'''

first_trending_date = format_trending_date(first_row['trending_date'])
first_publish_date  = format_publish_date(first_row['publish_time'])

video_stats = {
    'video_id':           first_row['video_id'],
    'trending_date':      format_trending_date(first_row['trending_date']),
    'publish_date':       format_publish_date(first_row['publish_time']),
    'title':              first_row['title'],
    'channel_title':      first_row['channel_title'],
    'category_id':        first_row['category_id'],
    'num_days_trending':  1,
    'days_till_trending': (first_trending_date - first_publish_date).days
}



for row in reader:

    if video_stats['video_id'] != row['video_id']:
        
        writer.writerow(video_stats)

        trending_date = format_trending_date(row['trending_date'])
        publish_date = format_publish_date(row['publish_time'])
        
        video_stats = {
            'video_id': row['video_id'],
            'trending_date': trending_date,
            'publish_date': publish_date,
            'title': row['title'],
            'channel_title': row['channel_title'],
            'category_id': row['category_id'],
            'num_days_trending': 1,
            'days_till_trending': (trending_date - publish_date).days
        }

    else:
        video_stats['num_days_trending'] += 1
        
    

'''

    Close files

'''

file_input.close()
file_output.close()