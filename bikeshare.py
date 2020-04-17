import time
import pandas as pd

CITY_DATA = { 'c': 'chicago.csv',
              'n': 'new_york_city.csv',
              'w': 'washington.csv' }

days = {'none': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}

months = {'none': 0,'january': 1, 'february': 2 , 'march': 3, 'april': 4, 'may': 5, 'june': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - the number corresponds to the month (January to June ) to filter by and 0 stands for no filter
        (int) day - the number corresponds to the day of week to filter by and none to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n ')

    while True:
        city = str(input("Enter the name of the city to analyze: Chicago, New York City, Washington\n")).lower()
        filters = str(input("Type (month, day, both, none), if you would like to filter the data by month, day, both or none for no filter. ")).lower()
        if filters == 'both':
            month = str(input("Enter the month(January to June) to filter by where none to apply no month filter\n ")).lower()
            day = str(input("Enter the day of week to filter by where  none to apply no day filter\n")).lower()

        elif filters == 'month':
            month = str(input("Enter the month(January to June) to filter by where none to apply no month filter\n ")).lower()
            day = 'none'
        elif filters == 'day':
            month = 'none'
            day = str(input("Enter the day of week(Monday to Sunday) to filter by where none to apply no day filter\n")).lower()
        else:
            month = 'none'
            day = 'none'

       # Check there are valid inputs

        if city not in ['chicago', 'new york city', 'washington']:
            print("\n Sorry your input is invalid. Please enter again values of city\n")

        elif month not in months.keys():
            print("\n Sorry your input is invalid. Please enter again values of month where it between 0 and 12\n")

        elif day not in days.keys():
            print("\n Sorry your input is invalid. Please enter again\n")

        else:
            print("\n Thanks for your information, we got the values correctly\n")

            break

    print('-'*40)
    print("The following filters will be applying in the calculation: month = {} and day = {}".format(month, day))
    print('-' * 40)
    return city[0], months[month], days[day]


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - the number corresponds to the month (January to June ) to filter by and 0 stands for no filter
        (int) day - the number corresponds to the day of week to filter by and none to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek + 1

    # filter by month if applicable
    if month != 0: # filter of month == 0 means no filter

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 0: # filter of day == 0 means no filter 
        
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day] # notice day of week starts 0 equals to monday, 1 to Tuesday and so on
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # the mode function returns a integer stands for month, using the global dictionary we get the name of month
    month_list = [month for month, num in months.items() if num == df['month'].mode()[0]]
    # Display the most common month
    print("The most common month: ", month_list[0].title())

    # the mode function returns a integer stands for day of week, using the global dictionary days we get the name
    day_list = [day for day, num in days.items() if num == df['day_of_week'].mode()[0]]
    # Display the most common day of week
    print("\nThe most common day of week:", day_list[0].title())

    # Display the most common start hour
    print("\nThe most common start hour:", df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("The most commonly used start station:", df['Start Station'].mode()[0])

    # Display most commonly used end station
    print("\nThe most commonly used end station:", df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    df = df.groupby(['Start Station','End Station']).size().reset_index(name='count')
    print("\nThe most frequent combination of start station and end station trip:\n",
          df.iloc[df['count'].idxmax()])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert(s):
    """
    Convert total_time in seconds to hour, minute
    :param s: times in seconds
    :return: (int) hours: convert the times s in format hours, minutes, seconds
             (int) minutes: convert the times s in format hours, minutes, seconds
             (int) seconds: convert the times s in format hours, minutes, seconds
    """

    hours = s // 3600
    minutes = (s % 3600) // 60
    seconds = (s % 3600) % 60

    return  hours, minutes, seconds

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    hours, minutes, seconds = convert(df['Trip Duration'].sum())
    print("the total travel time: {}h {}m {:.2f}s".format( hours, minutes, seconds))

    # display mean travel time
    hours, minutes, seconds = convert(df['Trip Duration'].mean())
    print("the mean travel time: {}h {}m {:.2f}s".format( hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    print(df.groupby(['User Type'])['User Type'].count())

    # display counts of gender and earliest, most recent, and most common year of birth only for Chicago and New York City
    if city != 'w':
        print("\n", df.groupby(['Gender'])['Gender'].count())
        print("\nThe most earliest year of birth\n ", int(df['Birth Year'].min()))
        print("The most recent year of birth\n ", int(df['Birth Year'].max()))
        print("The most common year of birth\n ", int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    while True:
        see_data = input('\nWould you like to view individual data? Enter yes or no.\n')
        if see_data.lower() == 'yes':
            print(df.head())
        else:
            break

def main():
    while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)

        # the following functions display statistic information
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    

