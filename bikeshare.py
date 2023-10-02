import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
OPTIONS = ['all', 'day', 'month', 'none']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]

def get_input(message, valid_list):
    """
    An utility function to obtain user specific input value

    Args:
        (str) message - an information message for a particular request
        (str) valid_list - a list of valid options
    Returns:
        (str) user_data - requested data from user
    """

    while True:
        user_data = input(message).lower()
        if user_data in valid_list:
            break
    
    return user_data

def get_city():
    '''
    This function starts the user interface by introduction and
    asking the user with the city he/she wants to analyze
    '''
    print("="*40)
    print('Welcome to Bikeshare Data Explorer!')
    print("="*40)
    print(' ')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Enter the city you want to analyze the data for:')
    print('Chicago: 1')
    print('New York: 2')
    print('Washington: 3')
    print(' ')
    city = input('Please choose the city for which you would like to see the Statistics: ')
    city = city.lower()
    while True:     # for handling the unexpected input by user
            if city == '1' or city == 'chicago':
                print("\nChicago City! Okay Let's go further\n")
                return 'chicago'
            if city == '2' or city == 'new york':
                print("\nNew York City! Okay let's go further\n")
                return 'new york city'
            elif city == '3' or city == 'washington':
                print("\nWashington! Okay let's go further\n")
                return 'washington'
            # error handled by implementing 'else' and provided another option to input data
            else:
                print('\nPlease enter 1, 2 or 3 or the names of cities\n')
                city = input('Please choose the city for which you would like to see the Statistics: ')
                city = city.lower()


def get_filters(city, month, day):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city()

    while True:
        time = get_input("Do you want to filter as month, day, all or none? ", OPTIONS).lower()               
        match time:
            case 'month':
                month = get_input("Which month? January, Feburary, March, April, May or June? ", MONTHS).lower()
                day = 'all'
                break
                    
            case 'day':
                month = 'all'
                day = get_input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? ", DAYS).lower()
                break
                    
            case 'all':
                month = get_input("Which month? January, Feburary, March, April, May or June? ", MONTHS).lower()           
                day = get_input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? ", DAYS).lower()
                break       
            case 'none':
                month = 'all'
                day = 'all'
                break       
            case _:
                print("You wrote the wrong word! Try Again\n")

    print(city)
    print(month)
    print(day)
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


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

    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



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

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print(total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print(mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(bike_users(df))

    # Display counts of gender
    if 'Gender' in df:
        print(gender_data(df))
    else:
        print("There is no gender information in this city.\n")

    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_years(df)
    else:
        print("There is no birth year information in this city.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""Asking 5 lines of the raw data and more, if they want"""
def data(df):
    raw_data = 0
    while True:
        answer = input("Do you want to see the raw data? Yes or No? ").lower()
        if answer not in ['yes', 'no']:
            answer = input("You wrote the wrong word. Please type Yes or No? ").lower()
        elif answer == 'yes':
            raw_data += 5
            print(df.iloc[raw_data : raw_data + 5])
            again = input("Do you want to see more? Yes or No? ").lower()
            if again == 'no':
                break
        elif answer == 'no':
            return


def main():
    city = ""
    month = ""
    day = ""
    while True:
        city, month, day = get_filters(city, month, day)
        df = load_data(city, month, day)

        # all the conclusions
        stats_funcs_list = [month_freq,
        day_freq, hour_freq, 
        ride_duration, common_trip, 
        stations_freq, bike_users, gender_data, birth_years]
	
        for x in stats_funcs_list:	# displays processing time for each function block
            process(x, df)
        
        disp_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no? ')
        if restart.lower() != 'yes':
            break

def birth_years(df):
    '''What is the earliest, latest, and most frequent birth year?'''
    # df - dataframe returned from time_filters
    try:
        print('\n* Q10. What is the earliest, latest, and most frequent year of birth, respectively?')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(int(earliest)) + "\n")
        latest = np.max(df['Birth Year'])
        print ("The latest year of birth is " + str(int(latest)) + "\n")
        most_frequent= df['Birth Year'].mode()[0]
        print ("The most frequent year of birth is " + str(int(most_frequent)) + "\n")
        return int(earliest), int(latest), int(most_frequent)
    except:
        print('No available birth date data for this period.')

def bike_users(df):
    '''What are the counts of each user type?
    '''
     # df - dataframe returned from time_filters
    print('\n* Q8. Types of users: subscribers, customers, others\n')
    return df['User Type'].value_counts()

def gender_data(df):
    '''What are the counts of gender?'''
    # df - dataframe returned from time_filters
    try:
        print('\n* Q9. What is the breakdown of gender among users?\n')
        return df['Gender'].value_counts()
    except:
        print('There is no gender data in the source.')

def disp_raw_data(df):
    '''
    Displays the data used to compute the stats
    Input:
        the df with all the bikeshare data
    Returns: 
       none
    '''
    #omit irrelevant columns from visualization
    #df = df.drop(['month', 'day_of_month'], axis = 1)
    row_index = 0

    see_data = input("\nYou like to see rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()
    while True:
        if see_data == 'no':
            return
        if see_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input("\n Would you like to see five more rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()

def month_freq(df):
    '''What is the most popular month for start time?
    '''
    # df - dataframe returned from time_filters
    print('\n * Q1. What is the most popular month for bike traveling?')
    #print(df.month.mode().empty)
    if df.month.mode().empty:
        return None
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[m - 1].capitalize()
    return popular_month

def day_freq(df):
    '''What is the most popular day of week for start time?
    '''
    # df - dataframe returned from time_filters
    print('\n * Q2. What is the most popular day of the week for bike rides?')
    if df['day_of_week'].value_counts().reset_index()['index'].empty:
        return None
    return df['day_of_week'].value_counts().reset_index()['index'][0]

def hour_freq(df):
    '''What is the most popular hour of day for start time?
    '''
    # df - dataframe returned from time_filters
    print('\n * Q3. What is the most popular hour of the day for bike rides?')
    df['hour'] = df['Start Time'].dt.hour
    if df.hour.mode().empty:
        return None
    return df.hour.mode()[0]

def ride_duration(df):
    '''
    What is the total ride duration and average ride duration?
    Result:
        tuple = total ride duration, average ride durations
    '''
    # df - dataframe returned from time_filters
    print('\n * Q4. What was the total traveling done for 2017 through June, and what was the average time spent on each trip?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #sum for total trip time, mean for avg trip time
    total_ride_time = np.sum(df['Travel Time'])
    total_days = str(total_ride_time).split()[0]

    print ("\nThe total travel time on 2017 through June was " + total_days + " days \n")
    avg_ride_time = np.mean(df['Travel Time'])
    avg_days = str(avg_ride_time).split()[0]
    print("The average travel time on 2017 through June was " + avg_days + " days \n")

    return total_ride_time, avg_ride_time

def stations_freq(df):
    '''What is the most popular start station and most popular end station?
    '''
    # df - dataframe returned from time_filters
    print("\n* Q5. What is the most popular start station?\n")
    if df['Start Station'].value_counts().reset_index()['index'].empty:
        return None
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print (start_station)
    print("\n* Q6. What is the most popular end station?\n")
    if df['End Station'].value_counts().reset_index()['index'].empty:
        return None
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    return start_station, end_station

def common_trip(df):
    '''What is the most popular trip?
    '''
    # df - dataframe returned from time_filters
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n* Q7. What was the most popular trip from start to end?')
    return result

def process(f, df):
    '''Calculates the time it takes to commpute a statistic
    '''
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computing this stat took %s seconds." % (time.time() - start_time))

if __name__ == "__main__":
	main()