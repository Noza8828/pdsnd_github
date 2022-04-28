import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Function to identify the user requirements
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
        city = input('Which city do you want to see statistics for: Chicago, New York or Washington? ').lower()
        if city not in CITY_DATA:
            print("\nInvalid answer. Please choose from the list provided\n")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        time = input("Do you want to filter by 'month', 'day', 'all' OR 'none'? ").lower()
        if time == 'month':
            month = input('Which month would like to see statistics for: January, Feburary, March, April, May or June? ').lower()
            day = 'all'
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
        elif time == 'day':
            month = 'all'
            day = input('Wich day would like to see statistics for: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? ').lower()
            break

    # get user input for all or none
        elif time == 'all':
            month = input('Which month would like to see statistics for: January, Feburary, March, April, May or June? ').lower()
            day = input('Wich day would like to see statistics for: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? ').lower()
            break
        elif time == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            input("The input was incorrect. Please choose from 'month', 'day', 'all' OR 'none'")
            break

    print('-'*40)
    return city, month, day

#Function to load data from .csv files
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

#Function to calculate time-related statistics for the chosen data
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print(common_month)

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print(common_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(common_hour)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

#Function to calculate station statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print(common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print(common_end)

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['combination'].mode()[0]
    print(common_combination)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

#Function to calculate trip duration statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print(total_duration)

    # display mean travel time
    avg_travel = df['Trip Duration'].mean()
    print(avg_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function to calculate user statistics
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print('There is no gender information in this city')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = df['Birth Year'].min()
        print(earliest)

        recent = df['Birth Year'].max()
        print(recent)

        common_birthdate = df['Birth Year'].mode()[0]
        print(common_birthdate)
    else:
        print('There is no birth year information in this city.')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


#Function to display the raw data as per user request
def display_data(df):
    """Displays 5 rows of data for the selected city."""

    response = ['yes', 'no']
    data = ''

    count = 0
    while data not in response:
        print('\nWould you like to view the raw data?')
        print('\nPlease answer either \nYes or \nNo')
        data = input().lower()
        #the raw data from the df is displayed if user opts for it
        if data == 'yes':
            print(df.head())
        elif data not in response:
            print('\nPlease answer either Yes or No.')

    #Extra while loop here to ask user if they want to continue viewing data
    while data == 'yes':
        print('Would you like to view more raw data?'')
        count += 5
        data = input().lower()
        #If user opts for it, this displays next 5 rows of data
        if data == 'yes':
             print(df[count:count + 5])
        elif data != 'yes':
             break
    print('-'*80)

#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
