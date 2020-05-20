import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

DAY_NUMS = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    try:
      city = input("From which city would you like information? Type chicago, new york city, or washington? \n").lower()
      while city not in CITY_DATA:
        print("There is something wrong with your entry, try again")
        city = input("From which city would you like information? Type chicago, new york city, or washington? \n").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
      month = input("From which month would you like information? Type all, january, february, ... , june \n").lower()
      while month not in MONTHS:
          print("There is something wrong with your entry, try again")
          month = input("From which month would you like information? Type all, january, february, ... , june \n").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
      day = input("From which day of the week would you like information? Type all, monday, tuesday, ... , sunday \n").lower()
      while day not in DAYS:
          print("There is something wrong with your entry, try again")
          day = input("From which day of the week would you like information? Type all, monday, tuesday, ... , sunday \n").lower()

    except Exception as e:
       print('An exception occurred with your inputs: {}'.format(e))

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == DAY_NUMS[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month_index = df['Start Time'].dt.month.mode()[0]
    common_month = MONTHS[common_month_index - 1]
    print("The most common month is: ", common_month)

    # TO DO: display the most common day of week
    common_day_index = df['day_of_week'].mode()[0]
    common_day = [dayname for dayname, number in DAY_NUMS.items() if number == common_day_index]
    day = " ".join(common_day)
    print("The most common day is: ", day)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour
    common_hour = df['hour'].mode()[0]
    print('The most common Start Hour is:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    common_start_trips = df['Start Station'].value_counts()[0]
    print("The most common Start Station is {} with {} trips".format(common_start_station, common_start_trips))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    common_end_trips = df['End Station'].value_counts()[0]
    print("The most common End Station is {} with {} trips".format(common_end_station, common_end_trips))

    # TO DO: display most frequent combination of start station and end station trip
    common_trip_df = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending = False)
    trip_number = common_trip_df.iloc[0]
    common_combo = common_trip_df[common_trip_df == trip_number].index[0]
    start, end = common_combo
    print("The most common trip is {} to {}, which was rode {} times".format(start, end, trip_number))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    trip_total = df['Trip Duration'].sum()
    trip_total = trip_total % (24 * 3600)
    trip_hours = trip_total // 3600
    trip_total %= 3600
    trip_minutes = trip_total // 60
    trip_total %= 60

    print("The total travel time is: {} hours, {} minutes, {} seconds".format(int(trip_hours), int(trip_minutes), int(trip_total)))

    # TO DO: display mean travel time
    trip_average = df['Trip Duration'].mean()
    trip_average = trip_average % (24 * 3600)
    avg_hours = trip_average // 3600
    trip_average %= 3600
    avg_minutes = trip_average // 60
    trip_average %= 60

    print("The average trip duration is: {} hours, {} minutes, {} seconds".format(int(avg_hours), int(avg_minutes), int(trip_average)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        type_user = df['User Type'].value_counts()
        print("The amount of Subscribers, Customers, etc is:\n{}\n".format(type_user))
    except Exception as ex:
        print("The counts for user types could not be identified. Exception: {}".format(ex))

    # Display counts of gender
    try:
        genders = df['Gender'].value_counts()
        print("The amount of Males and Females is:\n{}\n".format(genders))
    except Exception:
        print("The counts for each gender are not available.\n")

    # Display earliest, most recent, and most common year of birth
    try:
        birth_year = df['Birth Year']
        earliest = birth_year.min()
        print("The earliest birth year of users is {}.".format(int(earliest)))
        recent = birth_year.max()
        print("The most recent birth year of users is {}.".format(int(recent)))
        most_common = birth_year.mode()[0]
        print("The most common birth year is {}.".format(int(most_common)))
    except Exception:
        print("The data regarding birth year is not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays 5 rows of raw data upon request from the user"""
    count = 0
    while True:
        raw = input("Would you like to see raw data? Enter yes or no: ").lower()
        count += 1
        if raw == 'yes':
            if count == 1:
                print(df.iloc[:5])
            if count > 1:
                print(df.iloc[(count - 1) * 5: count * 5])
        if raw == 'no':
            break

    while False:
        print('There is something wrong with your entry. Enter yes or no:').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
