import time
import pandas as pd
import numpy as np
from os import system
from termcolor import colored

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = str()
    month = str()
    day = str()
    system('clear')
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['Chicago', 'New york city', 'Washington']
    while True:
        city_number = int(input(
            "Please specify which number of city to handle: \n(1)--> Chicago \n(2)--> New york city\n(3)--> Washington : "))
        city_index = city_number-1
        if city_index in [num for num, v in enumerate(cities)]:
            print('city is: {}'.format(cities[city_index]), '\n')
            city = cities[city_index].lower()
            break
        else:
            print('\nRe-choose correctly...')
            continue
    # get user input for month (all, january, february, ... , june)
    filter = input(
        'Would you like to filter the data by (m)-->month or (n)-->not, Please choose: ').lower()
    if filter == 'm':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        while True:
            month_choice = input(
                "Please choose which month to handle:" + colored("\t**any non-int answer will exit**", "green") + " \n"+colored((1), "blue")+"--> January, "+colored((2), "blue")+"--> February, "+colored((3), "blue")+"--> March, "+colored((4), "blue")+"--> Aapril, "+colored((5), "blue")+"--> May, "+colored((6), "blue")+"--> June, "+colored((0), "blue")+"-->All : ")
            try:
                month_number = int(month_choice)
                if month_number == 0:
                    print('month is: "All" months')
                    month = 'all'
                    break
                month_index = month_number-1
                if month_index in [num for num, v in enumerate(months)]:
                    print('month is: {} month'.format(
                        months[month_index]))
                    month = months[month_index]
                    break
                else:
                    print('\nRe-choose correctly,')
                    continue

            except ValueError as error:
                print('No Month is choosen')
                break
    else:
        print('No Month is choosen')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    filter = input(
        '\nWould you like to filter the data by (d)-->day or (n)-->not, Please choose: ').lower()
    if filter == 'd':
        days = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
        while True:
            try:
                day_choice = int(input(
                    "Please choose which day to handle:" + colored("\t**any non-int answer will exit**", "green") + " \n"+colored((1), "blue")+"--> Monday, "+colored((2), "blue")+"--> Tuesday, "+colored((3), "blue")+"--> Wednesday, "+colored((4), "blue")+"--> Thursday, "+colored((5), "blue")+"--> Friday, "+colored((6), "blue")+"--> Saturday, "+colored((7), "blue")+"-->Sunday : "))
                day_index = day_choice - 1
                if day_index in [num for num, v in enumerate(days)]:
                    print('day is: {} day'.format(
                        days[day_index]))
                    day = days[day_index]
                    break
                else:
                    print('\nRe-choose correctly,')
                    continue
            except ValueError as error:
                print('No day is choosen')
                break
    else:
        print('No day is choosen')

    print('-'*40)
    return [city, month, day]


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
    df['Month'] = df['Start Time'].dt.strftime('%B')
    df['Day'] = df['Start Time'].dt.strftime('%A')
    if month and day:
        df = df.query('Month == \"{}\" & Day == \"{}\"'.format(month, day))
    if month:
        df = df.query('Month == \"{}\"'.format(month))
    if day:
        df = df.query('Day == \"{}\"'.format(day))
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month:
        print("The most common month: ", colored("{}".format(month), "yellow"))
    else:
        most_common_month = ' '.join(df.Month.mode().values)
        print("The most common month: ", colored(
            "{}".format(most_common_month), "yellow"))

    # display the most common day of week
    if day:
        print("The most common day: ", colored("{}".format(day), "yellow"))
    else:
        most_common_day = ' '.join(df.Day.mode().values)
        print("The most common day: ", colored(
            "{}".format(most_common_day), "yellow"))

    # display the most common start hour
    most_common_hour = ' '.join(
        df['Start Time'].dt.strftime('%H').mode().values)
    print("The most common hour: ", colored(
        "{}".format(most_common_hour), "yellow"))

    print("\nThis took ", colored("{}".format(
        time.time() - start_time), "yellow"), " seconds.")
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = ' '.join(df['Start Station'].mode().values)
    print("The most common start station: ", colored(
        "{}".format(most_common_start_station), "yellow"))

    # display most commonly used end station
    most_common_end_station = ' '.join(df['End Station'].mode().values)
    print("The most common end station: ", colored(
        "{}".format(most_common_end_station), "yellow"))

    # display most frequent combination of start station and end station trip
    start_combination, end_combination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()

    print("The most common combination of start station and end station trip : \n{} --> ", colored("{}".format(
        start_combination, end_combination), "yellow"))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    # convert time in unit of seconds to equivalent reasonable unit
    def get_time_unit(time):
        units = [('seconds', 1), ('minutes', 60),
                 ('hours', 60), ('days', 24), ('weeks', 7), ('years', 52)]
        unit = None
        i = 0
        while time > units[i][1]:
            time /= units[i][1]
            unit = units[i][0]
            i += 1
            if i == len(units):
                break
        return (time, unit)
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time, total_unit = get_time_unit(total_travel_time)
    print("Total travel time: ", colored(
        "{} {}".format(total_travel_time, total_unit), "yellow"))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time, mean_unit = get_time_unit(mean_travel_time)
    print("Mean travel time: ", colored(
        "{} {}".format(mean_travel_time, mean_unit), "yellow"))

    print("\nThis took ", colored("{}".format(
        time.time() - start_time), "yellow"), " seconds.")
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:")
    counts_user = dict(df['User Type'].value_counts())
    for count in counts_user.items():
        print(colored("\t{}: {}".format(count[0], count[1]), 'yellow'))
    print()
    # Display counts of gender
    print("Counts of gender:")
    # handle loosing data in some city
    if city == 'washington':
        print("Sorry there is not data available for Gender and Birth year")
    else:
        counts_gender = dict(df['Gender'].value_counts())
        for count in counts_gender.items():
            print(colored("\t{}: {}".format(count[0], count[1]), 'yellow'))

        print()
        # Display earliest, most recent, and most common year of birth
        print("Statistics on year of birth:")
        # data series of Birth Year columns
        year_birth = df['Birth Year']
        print("\tThe earliest year of birth: ", colored(
            "{}".format(int(year_birth.min())), 'yellow'))
        print("\tThe most recent year of birth: ", colored(
            "{}".format(int(year_birth.max())), 'yellow'))
        print("\tThe most common year of birth: ", colored(
            "{}".format(int(year_birth.mode())), 'yellow'))

        print("\nThis took ", colored("{}".format(
            time.time() - start_time), "yellow"), " seconds.")
    print('-'*40)


def print_raw_data(df):
    """Display chunk of 5 rows of data frame repeatedly"""
    while True:
        response = input(
            "Would you like to display raw data ? type: yes(y) / other thing: ")
        if response.lower() not in ['yes', 'y']:
            break
        print(df.head())
#         reassign new data frame (start from 5th row to the last row including all columns) which is sliced from the original data frame
        df = df.iloc[5:, ]


def main():
    while True:
        city, month, day = get_filters()
        if month == '' or month == 'all':
            month = None
        if not day:
            day = None
        df = load_data(city, month, day)

        time_stats(df, month, day)
        df = df.drop(['Month', 'Day'], axis=1)

        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        print_raw_data(df)
        restart = input(
            '\nWould you like to restart? Enter yes(y) or no(another thing).\n')
        if restart.lower() not in ['yes', 'y']:
            print(colored('Exit', 'red'))
            break
            exit()


if __name__ == "__main__":
    main()
