# main.py

"""Random variables:
    patient numbers per hour
    the time point each patient arrives in one hour
    either a patient comes to only see a nurse or both a nurse and a doctor
    the time spending with a nurse and a doctor of a patient
    """

import random
import numpy as np
import pandas as pd
from scipy.stats import truncnorm
from time import clock


"""Build the distribution of time spent with a nurse or a doctor"""


class TimeDistribution:
    """
    Build the normal distribution of the time spent by a patient with a nurse or a doctor
    """

    def __init__(self, mean_t=0, sd=0, min_t=0, max_t=0, num=0):
        self.mean = mean_t
        self.sd = sd
        self.min = min_t
        self.max = max_t
        self.num = num

    # Return a list of time following normal distribution
    def time_spend(self) -> list:
        generator = truncnorm((self.min-self.mean)/self.sd, (self.max-self.mean)/self.sd, loc=self.mean, scale=self.sd)
        time = generator.rvs(self.num)
        return time

    # Returns the sum of the list of time
    def sum_truncnorm(self) -> float:
        generator = truncnorm((self.min - self.mean) / self.sd, (self.max - self.mean) / self.sd, loc=self.mean, scale=self.sd)
        time = generator.rvs(self.num)
        return sum(time)


"""Calculate the utilization of the nurses and doctors in one hour"""


def utilization(mean_t, sd, min_t, max_t, nurse: int, doctor: int, patient: int, patient_both: int):
    """
    Calculates the utilization of the nurses and doctors in one hour

    :param mean_t: mean time (minutes) of the seeing nurse & doctor time distribution
    :param sd: standard deviation of the seeing nurse & doctor time distribution
    :param min_t: min time (minutes) of the seeing nurse & doctor time distribution
    :param max_t: max time (minutes) of the seeing nurse & doctor time distribution
    :param nurse: given number of nurses
    :param doctor: given number of doctors
    :param patient: given number of all of the patients
    :param patient_both: number of patients who see both a nurse and a doctor, less than total patients number
    :return: a tuple with the utilization values of nurses and doctors
    """

    # Calculate the total time (minutes) nurses and doctors need to work with patients in one hour
    total_nurse_time = TimeDistribution(mean_t, sd, min_t, max_t, patient).sum_truncnorm()
    total_doctor_time = TimeDistribution(mean_t, sd, min_t, max_t, patient_both).sum_truncnorm()

    # Calculate the utilization values to return
    utilization_nurse = total_nurse_time / (nurse * 60)
    utilization_doctor = total_doctor_time / (doctor * 60)

    return utilization_nurse, utilization_doctor


"""Calculate the average and max waiting time for a nurse and a doctor of patients, create a dataframe storing every
    patient's time spend data, and two arrays of nurses and doctors, iterating and storing their working time during 
    the process"""


def wait_time(mean_t, sd, min_t, max_t, nurse, doctor, patient, patient_nurse, patient_both):
    """
    Calculate the average and max waiting time for a nurse and a doctor of a patient

    :param mean_t: mean time (minutes) of the seeing nurse & doctor time distribution
    :param sd: standard deviation of the seeing nurse & doctor time distribution
    :param min_t: min time (minutes) of the seeing nurse & doctor time distribution
    :param max_t: max time (minutes) of the seeing nurse & doctor time distribution
    :param nurse: given number of nurses
    :param doctor: given number of doctors
    :param patient: given number of all of the patients
    :param patient_nurse: number of patients who only see a nurse, less than total patients number
    :param patient_both: number of patients who see both a nurse and a doctor, less than total patients number
    :return: a tuple with the average and max waiting time for nurses and doctors of patients
    """

    """Create a dataframe with a list of patient as index, storing the time point data and time spent length data of 
       each patient"""

    # Create a list of patient as [patient_1, patient_2, ..., patient_totalnumberofpatients], in order
    list_patient = []
    for i in range(patient):
        list_patient.append('patient_{}'.format(i+1))

    # The list of data as index, all initial time data as 0, and assume all patients to see both a nurse and a doctor
    df_patients = pd.DataFrame({'Arrival_point': 0, 'Nurse_only': False,
                                'Waiting_nurse': 0, 'Meet_nurse_point': 0,
                                'Seeing_nurse': 0, 'After_nurse_point': 0,
                                'Waiting_doctor': 0, 'Meet_doctor_point': 0,
                                'Seeing_doctor': 0, 'After_doctor_point': 0}, index=list_patient)


    """Deal with 'Arrival_point', 'Nurse_only', 'Seeing_nurse' columns, for all patients"""

    # Create a list of random numbers that sum to 60
    # Use this list of numbers as the gap (minutes) of the arrival point between every two patients in one hour
    # Assume the starting point as 0, then add the numbers as the Arrival_point of each patient, such as
    # For the first patient it's 0 plus the first number, for the second patient it's 0 plus the first and second number
    total_time = 60
    random_arrival = [random.random() for i in range(patient)]
    sum_arrival = sum(random_arrival)
    arrival_time = [total_time * i / sum_arrival for i in random_arrival]
    for i in range(patient):
        df_patients.loc[list_patient[i], 'Arrival_point'] += sum(arrival_time[:i])

    # Randomly select certain number of patients from the ordered patient list by their ordinal numbers
    # Use these selected patients as people only come to see a nurse, put their ordinal numbers in a list
    # Change the cells of 'Nurse_only' column of certain patients based on the ordinal numbers selected to this list
    list_patient_nurse_num = random.sample(list(range(patient)), patient_nurse)
    for i in list_patient_nurse_num:
        df_patients.loc['patient_{}'.format(i + 1), 'Nurse_only'] = True

    # Get a list of patients numbers of random floats, as the different time spending with a nurse of each patient,
    # following normal distribution
    # Assign this list of time values to the 'Seeing_nurse' column of the dataframe
    df_patients['Seeing_nurse'] = TimeDistribution(mean_t, sd, min_t, max_t, patient).time_spend()


    """Create two nurse and doctor arrays, deal with 'Meet_nurse_point', 'Waiting_nurse', 'After_nurse_point' columns, 
       for all patients, update nurse array"""

    # Create two arrays for nurses and doctors, item numbers equal to numbers of nurses and doctors respectively
    # Each item represents the available time point of a nurse or a doctor
    # Assuming starting point is 0 (initial values), every nurse and doctor is available
    # Later, add the time a nurse or doctor spent with a patient while iterating the patients (df index)
    # After the accumulation, the updated value indicates the new time point that nurse or doctor is available again
    arr_nurse = np.zeros(nurse)
    arr_doctor = np.zeros(doctor)

    for i in range(patient):

        # Compare the min value in nurse array and the arrival point of each patient
        # If formar <= latter, indicates a nurse immediately available, the patient's 'Meet_nurse_point' = 'Arrival_point'
        # Otherwise, his/her 'Meet_nurse_point' = minnurse available point in the array
        if min(arr_nurse) <= df_patients.loc[list_patient[i], 'Arrival_point']:
            df_patients.loc[list_patient[i], 'Meet_nurse_point'] = df_patients.loc[list_patient[i], 'Arrival_point']
        else:
            df_patients.loc[list_patient[i], 'Meet_nurse_point'] = min(arr_nurse)

        # Then, the patient's 'Waiting_nurse' time period = 'Meet_nurse_point' - 'Arrival_point'
        # 'After_nurse_point' = 'Meet_nurse_point' + 'Seeing_nurse' time period
        df_patients.loc[list_patient[i], 'Waiting_nurse'] = df_patients.loc[list_patient[i], 'Meet_nurse_point'] - df_patients.loc[list_patient[i], 'Arrival_point']
        df_patients.loc[list_patient[i], 'After_nurse_point'] = df_patients.loc[list_patient[i], 'Meet_nurse_point'] + df_patients.loc[list_patient[i], 'Seeing_nurse']

        # Update the value of the nurse in the array, store his/her next available point in the array
        arr_nurse[np.argmin(arr_nurse)] += df_patients.loc[list_patient[i], 'Seeing_nurse']


    """Deal with 'Meet_doctor_point', 'Waiting_doctor', 'Seeing_doctor', 'After_nurse_point' columns, for all patiencts,
       update doctor array during iterating, similar to nurse columns"""

    # Select patients only to see a nurse, put None to their doctor-related cells
    list_patient_nurse = [p for p in df_patients[df_patients['Nurse_only'] == True].index]
    for i in range(patient_nurse):
        df_patients.loc[list_patient_nurse[i], 'Waiting_doctor':'After_doctor_point'] = None

    # Randomly put time periods to the 'See_doctor' cells of people to see a doctor, similar to 'Seeing_nurse' column
    list_patient_both = [p for p in df_patients[df_patients['Nurse_only'] == False].index]
    time_doctor = TimeDistribution(mean_t, sd, min_t, max_t, patient_both).time_spend()
    for i in range(patient_both):
        df_patients.loc[list_patient_both[i], 'Seeing_doctor'] = time_doctor[i]

    for i in range(patient_both):

        # Compare the min value in doctor array and the After_nurse_point of each patient, get 'Meet_doctor_point'
        if min(arr_doctor) <= df_patients.loc[list_patient_both[i], 'After_nurse_point']:
            df_patients.loc[list_patient_both[i], 'Meet_doctor_point'] = df_patients.loc[list_patient_both[i], 'After_nurse_point']
        else:
            df_patients.loc[list_patient_both[i], 'Meet_doctor_point'] = min(arr_doctor)

        # Then, the patient's 'Waiting_doctor' time period = 'Meet_doctor_point' - 'After_nurse_point'
        # 'After_doctor_point' = 'Meet_doctor_point' + 'Seeing_doctor' time period
        df_patients.loc[list_patient_both[i], 'Waiting_doctor'] = df_patients.loc[list_patient_both[i], 'Meet_doctor_point'] - df_patients.loc[list_patient_both[i], 'After_nurse_point']
        df_patients.loc[list_patient_both[i], 'After_doctor_point'] = df_patients.loc[list_patient_both[i], 'Meet_doctor_point'] + df_patients.loc[list_patient_both[i], 'Seeing_doctor']

        # Update the value of the doctor in the array, store his/her next available point in the array
        arr_doctor[np.argmin(arr_doctor)] += df_patients.loc[list_patient_both[i], 'Seeing_doctor']


    """After building the dataframs, get the average and max values of Waiting_nurse and Wating_doctor columns to return"""

    average_wait_nurse = round(df_patients['Waiting_nurse'].mean(), 2)
    max_wait_nurse = round(df_patients['Waiting_nurse'].max(), 2)
    average_wait_doctor = round(df_patients['Waiting_doctor'].sum() / patient_both, 2)
    max_wait_doctor = round(df_patients['Waiting_doctor'].max(), 2)

    return average_wait_nurse, max_wait_nurse, average_wait_doctor, max_wait_doctor


"""Run the simulation"""


def simulation(nurse, doctor, patient, sample):
    """
    Simulate the situation to get both utilization of nurses and nurses, and average and max waiting time values
    :param nurse: given number of nurses
    :param doctor: given number of doctors
    :param patient: the approximate number of patients per hours
    :param sample: simulate times
    :return:
    """
    # Get the random number of patients, assume 20% of them only to see the nurses
    patient = random.randint(patient - 5, patient + 5)
    patient_nurse = int(patient * 0.2)
    patient_nurse_doctor = patient - patient_nurse

    # (mean, sd, min, max) variables indicating the time(minutes) a patient needs to spent with a nurse/doctor
    mean_time = random.randint(25, 35)
    sd = 1
    min_time = mean_time - 10
    max_time = mean_time + 10

    # Run both utilization and waiting time multiple times, get lists of the results respectivelt
    ut_nurse, ut_doctor, ave_nurse, max_nurse, ave_doctor, max_doctor = [], [], [], [], [], []
    for i in range(sample):
        ut_n, ut_d = utilization(mean_time, sd, min_time, max_time, nurse, doctor, patient, patient_nurse_doctor)
        ut_nurse.append(ut_n)
        ut_doctor.append(ut_d)
        ave_n, max_n, ave_d, max_d = wait_time(mean_time, sd, min_time, max_time, nurse, doctor, patient, patient_nurse, patient_nurse_doctor)
        ave_nurse.append(ave_n)
        max_nurse.append(max_n)
        ave_doctor.append(ave_d)
        max_doctor.append(max_d)

    # Get the mean values of these lists of results as final results to print
    utilization_nurse = round(np.mean(ut_nurse) * 100, 2)
    utilization_doctor = round(np.mean(ut_doctor) * 100, 2)
    average_nurse = round(np.mean(ave_nurse), 2)
    max_wait_nurse = round(np.mean(max_nurse), 2)
    average_doctor = round(np.mean(ave_doctor), 2)
    max_wait_doctor = round(np.mean(max_doctor), 2)

    print('\n\nAfter {} times of simulation:'.format(sample))
    print("\nThe utilization of nurse is {}%".format(utilization_nurse))
    print("The utilization of doctor is {}%".format(utilization_doctor))
    print('\nThe average and maximum waiting time for nurse are {} minutes and {} minutes'.format(average_nurse, max_wait_nurse))
    print('The average and maximum waiting time for doctor are {} minutes and {} minutes'.format(average_doctor, max_wait_doctor))

    return None


def main():

    clock()

    print('\nWhen there are 8 nurses, 4 doctors, and around 20 patients per hour:')
    for i in [20, 200, 2000, 20000]:  # Run the similuation for 20, 200, 2000, 20000 times
        simulation(8, 4, 20, i)

    print('\nTotal running time is %-1.5ss' % clock())


if __name__ == '__main__':

    # with open('Output.txt', 'w') as outfile:
    main()

