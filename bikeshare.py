import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = str(input("\nEnter a city (chicago,new york city or washington): ").strip().lower())
        if city not in CITY_DATA.keys():
            print("\nInvalid response. Pick a valid city from the given options")
            continue
        else:
            print("\nSelected data file for {}".format(city))
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("Pick a month (all, january, february, march, april, may, june): ").strip().lower())
        if month not in ("all", "january", "february", "march", "april", "may", "june"):
            print("\nInvalid Response. Please pick from the given options")
            continue
        else:
            print("\nSelected {}".format(month))
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("Pick a day (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ").strip().lower())
        if day not in ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
            print("\nInvalid Response. Please pick  from the given options")
            continue
        else:
            print("\nSelected {}".format(day))
            break

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month: {}'.format(popular_month))

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day: {}'.format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: {}'.format(popular_hour))

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station: {}'.format(popular_start_station))

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['routes'] = df['Start Station'] + " - " + df['End Station']
    popular_route = df['routes'].mode().values[0]
    route_frequency = df['routes'].value_counts().max()
    print('The Most Popular Route: {} ({})'.format(popular_route, route_frequency))

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("\nTotal travel Time: {}".format(total_travel_time))

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time: {}".format(mean_travel_time))


    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)


    # Display counts of gender
    if "Gender" in df.columns:
        gender_frequency = df['Gender'].value_counts()
        print(gender_frequency)
    else:
        print("\nThis dataset does not have the column called 'Gender'")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("\nEarliest birth year: '{}'. \nMost recent birth year: '{}'. \nMost common birth year: '{}'.".format(earliest, most_recent, most_common))
    else:
        print("\nThis dataset does not have the column called 'Birth Year'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data 5 rows at a time."""

    start_time = time.time()
    start = 0
    while True:
        show_raw_data = input("\nWould you like to see individual raw data? Enter 'yes' or 'no'\n").strip().lower()
        if show_raw_data not in ("yes", "no", 'y', 'n'):
            print("Invalid response. Please type in 'yes' or 'no'")
            continue
        elif show_raw_data in ("yes", "y"):
            print('\nGetting raw data...\n')
            print(df.iloc[0:5,:])
            show_next_five = input("\nWould you like to see the next 5 rows?")
            if show_next_five in ("yes", "y"):
                start += 5
                if (start + 5 >= len(df.index)):
                    print(df.iloc[start:len(df.index) - 1, :])
                    print("You've reached the end of the data")
                    break
                print(df.iloc[start: start+5, :])
            else:
                break
        else:
            print("You have chosen not to see the individual data")
            break
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


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
        if restart.lower() not in ("yes", 'y'):
            break


if __name__ == "__main__":
	main()
