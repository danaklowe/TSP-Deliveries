import datetime


# converts user input to datetime object which corresponds to end_time for each truck's route processing algorithm.
# space-time complexity: O(1)
def delivery_status_timer():
    start_date = datetime.date.today()
    # start_time = datetime.time(8, 0, 0)
    # start_date_time = datetime.datetime.combine(start_date, start_time)

    end_date = start_date
    while True:
        entry_string = input('To check delivery status, enter time in format HHMM between 0800 & 1700 (enter \'q\' to '
                             'exit): ')
        if entry_string == 'q' or entry_string == 'Q':
            exit()

        end_time = None
        try:
            end_time = datetime.datetime.strptime(entry_string, "%H%M")
        except ValueError:
            print('Please enter time in a valid format of HHMM')
        if end_time is not None:
            end_time_hr = end_time.hour
            end_time_min = end_time.minute
            end_time_final = datetime.time(end_time_hr, end_time_min, 0, 0)

            if (end_time_hr in range(8, 17) and end_time_min in range(0, 60)) or \
                    (end_time_hr == 17 and end_time_min == 0):
                print("Checking delivery status as of {0:02d}:{1:02d}...\n".format(end_time_hr, end_time_min))
                end_date_time = datetime.datetime.combine(end_date, end_time_final)
                return end_date_time
            else:
                print('Please enter a valid time between 0800 & 1700.')
