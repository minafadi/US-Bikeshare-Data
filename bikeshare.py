import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITIES = list(CITY_DATA.keys())
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Filter by city: Select a city (chicago, new york city, washington): ').lower()
        if city not in CITIES:
            print('Please select a city from given above!')
            continue
        else: break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Filter by month: Select a month (all, january, february, march, april, may, june): ').lower()
        if month not in MONTHS:
            print('Please select a month given above!')
            continue
        else: break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Filter by day: Select a day (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ').lower()
        if day not in DAYS:
            print('Please select a day from given above!')
            continue
        else: break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Year'] = df['Start Time'].dt.year
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    df['Start-End Stations'] = df['Start Station'] + ' - ' + df['End Station']
    df['trip_duration'] = ((df['End Time'] - df['Start Time']).dt.total_seconds())/60   # in minutes

    if month != 'all':
        df = df[df['Month'] == month.title()]
    if day != 'all':
        df = df[df['Day'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]
    print('The most common month is: {}.'.format(common_month))

    # display the most common day of week
    common_day = df['Day'].mode()[0]
    print('The most common day of week is: {}.'.format(common_day))

    # display the most common start hour
    common_start_hour = df['Hour'].mode()[0]
    print('The most common start hour is: {}.'.format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: {}.'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: {}.'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_start_end = df['Start-End Stations'].mode()[0]
    print('The most frequent combination of start-end stations trip is: {}.'.format(common_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (sum(df['trip_duration']))/60   # in hours
    print('The total travel time is: {} hours.'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = (df['trip_duration'].mean())  # in minutes
    print('The average travel time is: {} minutes.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    subscibers_count = (df['User Type'] == 'Subscriber').sum()
    customers_count = (df['User Type'] == 'Customer').sum()
    print('Number of subscribers is: {}.'.format(subscibers_count))
    print('Number of customers is: {}.'.format(customers_count))

    # Display counts of gender
    if 'Gender' in df.columns:
        male_count = (df['Gender'] == 'Male').sum()
        female_count = (df['Gender'] == 'Female').sum()
        print('Number of males is: {}.'.format(male_count))
        print('Number of females is: {}.'.format(female_count))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print('Earliest year of birth is: {}.'.format(earliest_year))
        print('Most recent year of birth is: {}.'.format(most_recent_year))
        print('Most common year of birth is: {}.'.format(most_common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print('You selected to filter with city: {}, month(s): {}, day(s): {}'.format(city, month, day))

        df = load_data(city, month, day)
        display_dataset = input('Do you want to display the first 5 rows of the filtered dataset? ')
        for i in range(5,len(df),5):
            if display_dataset.lower() == 'yes':
                print(df.head(i))
                display_dataset = input('Do you want to display more rows? ')
            else: break
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
