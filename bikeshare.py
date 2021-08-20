import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("Would you like to see data for Chicago, New York City, or Washington? \n").lower()
    while city not in CITY_DATA.keys():
        city = input("Please select one of the following Chicago, New York City, or Washington? \n").lower()

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input("Would you like to view 'all' months or select from 'january', 'february', 'march', 'april', 'may',"
                  " or 'june' \n").lower()
    while month not in months:
        month = input(
            "Please select one of the following ('all, 'january', 'february', 'march', 'april', 'may', or 'june') \n").\
            lower()

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input("Would you like to view 'all' days or select from 'monday', 'tuesday', 'wednesday', 'thursday', "
                "'friday', 'saturday', or 'sunday' \n").lower()
    while day not in days:
        day = input(
            "Please select one of the following ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', "
            "'saturday', or 'sunday') \n").lower()

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
    df = pd.read_csv(CITY_DATA.get(city))
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[(df['month'] == month)]

    # filter by day of week if applicable
    if day != 'all':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = days.index(day.title())
        # filter by day of week to create the new dataframe
        df = df.loc[(df['day_of_week'] == day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    month = df['month'].mode()[0]
    day = df['day_of_week'].mode()[0]
    start_hour = df['start_hour'].mode()[0]
    print('The most common month is {}, The count of occurrences is {} times'.
          format(months[month-1], df['month'].value_counts()[month]))

    print('The most common day is {}, The count of occurrences is {} times'.
          format(days[day], df['day_of_week'].value_counts()[day]))

    print('The most common start hour is {}, The count of occurrences is {} times'.
          format(start_hour, df['start_hour'].value_counts()[start_hour]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    start_station = df['Start Station'].mode()[0]
    end_station = df['End Station'].mode()[0]
    df['Start to End'] = df['Start Station'] + " - " + df['End Station']
    start_end = df['Start to End'].mode()[0]
    print('The most common used start station is {}, The count of occurrences is {} times'.
          format(start_station, df['Start Station'].value_counts()[start_station]))
    print('The most common used end station is {}, The count of occurrences is {} times'.
          format(end_station, df['End Station'].value_counts()[end_station]))
    print('The most frequent combination is {}, The count of occurrences is {} times'.
          format(start_end, df['Start to End'].value_counts()[start_end]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("The total travel time is: {} Sec.".format(df['Trip Duration'].sum()))
    print("The mean travel time is: {} Sec.".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()

    if 'Gender' in df.columns:
        gender = "\nThe counts of gender: \n{}".format(df['Gender'].value_counts())
    else:
        gender = "\nNo gender information available for this city!"

    if 'Birth Year' in df.columns:
        birth_year = "\nThe year of birth: \nEarliest: {}\nMost recent: {}\nMost common: {}"\
            .format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0]))
    else:
        birth_year = "\nNo year of birth information available for this city!"

    print("The counts of user types: \n{}".format(user_types))
    print(gender)
    print(birth_year)

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
        raw_data_view = input('\nWould you view individual trip data? Enter yes or no.\n').lower()
        minimum = 0
        maximum = 5
        while raw_data_view == 'yes':
            print(df.iloc[minimum:maximum])
            print('\nAvailable data records are: {} rows'.format(df.shape[0]))
            minimum += 5
            maximum += 5
            if maximum > df.shape[0]:
                print("\nYou have reached the end of the Dataset!")
                raw_data_view = 'no'
            else:
                raw_data_view = input('\nWould you view individual trip data? Enter yes or no.\n').lower()
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
