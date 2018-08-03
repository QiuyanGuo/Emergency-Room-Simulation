# main.py

import random
import numpy as np
import pandas as pd
from scipy.stats import truncnorm
from time import clock


"""Build the distribution of time spent with a nurse or a doctor"""


class TimeDistribution:
    """
    Build the normal distribution of the time spent by a patient with a nurse or a doctor, time_spend function returns a
    list of time following normal distribution, sum_truncnorm returns the sum of the list of time

    """

    def __init__(self, mean_t=0, sd=0, min_t=0, max_t=0, num=0):
        self.mean = mean_t
        self.sd = sd
        self.min = min_t
        self.max = max_t
        self.num = num

    def time_spend(self) -> list:
        generator = truncnorm((self.min-self.mean)/self.sd, (self.max-self.mean)/self.sd, loc=self.mean, scale=self.sd)
        time = generator.rvs(self.num)
        return time

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

    # calculate the total time (minutes) nurses and doctors need to work with patients in one hour
    total_nurse_time = TimeDistribution(mean_t, sd, min_t, max_t, patient).sum_truncnorm()
    total_doctor_time = TimeDistribution(mean_t, sd, min_t, max_t, patient_both).sum_truncnorm()

    # utilization
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


    # Create a list of patient as [patient_1, patient_2, ..., patient_totalnumberofpatients], in order

    list_patient = []
    for i in range(patient):
        list_patient.append('patient_{}'.format(i+1))


    # Create a dataframe with the list of patient as index, all initial time data as 0, and assume all patients to
    # see both a nurse and a doctor

    df_patients = pd.DataFrame({'Arrival_point': 0, 'Nurse_only': False,
                                'Waiting_nurse': 0, 'Meet_nurse_point': 0,
                                'Seeing_nurse': 0, 'After_nurse_point': 0,
                                'Waiting_doctor': 0, 'Meet_doctor_point': 0,
                                'Seeing_doctor': 0, 'After_doctor_point': 0}, index=list_patient)


    # Create a list of random number that sum to 60, which is used to be the list of the gap (minutes) of the arrival
    # time between every two patients in one hour
    # Assume the starting point as 0, then the arrival point of each patient is the accumulative value of numbers of gap
    # time, such as the arrival point of the first patient is 0 plus the value of the first item in the list, and that
    # of the second patient is the first arrival time plus the value of the second item

    total_time = 60
    random_arrival = [random.random() for i in range(patient)]
    sum_arrival = sum(random_arrival)
    arrival_time = [total_time * i / sum_arrival for i in random_arrival]
    for i in range(patient):
        df_patients.loc[list_patient[i], 'Arrival_point'] += sum(arrival_time[:i])


    # Randomly select certain number of patients from the ordered patient list with their ordinal numbers, as people
    # only seeing a nurse, put them in a list, and based on this list, change the cells of 'Nurse_only' column of these
    # patients to True

    list_patient_nurse = random.sample(list(range(patient)), patient_nurse)
    for i in list_patient_nurse:
        df_patients.loc['patient_{}'.format(i + 1), 'Nurse_only'] = True


    # Create two arrays for nurses and doctors with same numbers of items as the numbers of nurses and doctors
    # respectively, each item represents the available time point of a nurse or a doctor
    # The initial values are all 0 (assuming the starting point is 0), every nurse and doctor is available, then each
    # item's value will add the time a nurse or doctor spent with a patient, each time after the accumulation indicates
    # the time point that each nurse and doctor is available again

    arr_nurse = np.zeros(nurse)
    arr_doctor = np.zeros(doctor)


    # Get a list of patients numbers of random floats, as the different time spending with a nurse of each patient,
    # following normal distribution
    # Assign this list of time values to the 'Seeing_nurse' column of the dataframe

    df_patients['Seeing_nurse'] = TimeDistribution(mean_t, sd, min_t, max_t, patient).time_spend()


    # Com

    for i in range(patient):
        if min(arr_nurse) <= df_patients.loc[list_patient[i], 'Arrival_point']:
            df_patients.loc[list_patient[i], 'Meet_nurse_point'] = df_patients.loc[list_patient[i], 'Arrival_point']
        else:
            df_patients.loc[list_patient[i], 'Meet_nurse_point'] = min(arr_nurse)
        df_patients.loc[list_patient[i], 'Waiting_nurse'] = df_patients.loc[list_patient[i], 'Meet_nurse_point'] - df_patients.loc[list_patient[i], 'Arrival_point']
        df_patients.loc[list_patient[i], 'After_nurse_point'] = df_patients.loc[list_patient[i], 'Meet_nurse_point'] + df_patients.loc[list_patient[i], 'Seeing_nurse']

        arr_nurse[np.argmin(arr_nurse)] += df_patients.loc[list_patient[i], 'Seeing_nurse']

    list_nurseonly_patient = [p for p in df_patients[df_patients['Nurse_only'] == True].index]
    for i in range(patient_nurse):
        df_patients.loc[list_nurseonly_patient[i], 'Waiting_doctor':'After_doctor_point'] = None

    list_mix_patient = [p for p in df_patients[df_patients['Nurse_only'] == False].index]
    time_doctor = TimeDistribution(mean_t, sd, min_t, max_t, patient_both).time_spend()
    for i in range(patient_both):
        df_patients.loc[list_mix_patient[i], 'Seeing_doctor'] = time_doctor[i]

    for i in range(patient_both):
        if min(arr_doctor) <= df_patients.loc[list_mix_patient[i], 'After_nurse_point']:
            df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] = df_patients.loc[list_mix_patient[i], 'After_nurse_point']
        else:
            df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] = min(arr_doctor)
        df_patients.loc[list_mix_patient[i], 'Waiting_doctor'] = df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] - df_patients.loc[list_mix_patient[i], 'After_nurse_point']
        arr_doctor[np.argmin(arr_doctor)] += df_patients.loc[list_mix_patient[i], 'Seeing_doctor']
        df_patients.loc[list_mix_patient[i], 'After_doctor_point'] = df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] + df_patients.loc[list_mix_patient[i], 'Seeing_doctor']

    average_wait_nurse = round(df_patients['Waiting_nurse'].mean(), 2)
    max_wait_nurse = round(df_patients['Waiting_nurse'].max(), 2)
    average_wait_doctor = round(df_patients['Waiting_doctor'].sum() / patient_both, 2)
    max_wait_doctor = round(df_patients['Waiting_doctor'].max(), 2)

    return average_wait_nurse, max_wait_nurse, average_wait_doctor, max_wait_doctor


def simulation(nurse, doctor, patient, sample):

    patient = random.randint(patient - 5, patient + 5)  # random variable
    patient_nurse = int(patient * 0.2)  # patients only to see nurse
    patient_nurse_doctor = patient - patient_nurse  # patients to see nurse & doctor

    # (mean, sd, min, max) random variables indicating the time(minutes) a patient needs to spent with a nurse/doctor
    mean_time = random.randint(25, 35)
    sd = 1
    min_time = mean_time - 10
    max_time = mean_time + 10

    ut_nurse, ut_doctor, ave_nurse, max_nurse, ave_doctor, max_doctor = [], [], [], [], [], []

    for i in range(sample):
        ut_n, ut_d = utilization(mean_time, sd, min_time, max_time, nurse, doctor, patient, patient_nurse_doctor)
        ut_nurse.append(ut_n)
        ut_doctor.append(ut_d)
        ave_n, max_n, ave_d, max_d = \
            wait_time(mean_time, sd, min_time, max_time, nurse, doctor, patient, patient_nurse, patient_nurse_doctor)
        ave_nurse.append(ave_n)
        max_nurse.append(max_n)
        ave_doctor.append(ave_d)
        max_doctor.append(max_d)

    utilization_nurse = round(np.mean(ut_nurse) * 100, 2)
    utilization_doctor = round(np.mean(ut_doctor) * 100, 2)
    average_nurse = round(np.mean(ave_nurse), 2)
    max_wait_nurse = round(np.mean(max_nurse), 2)
    average_doctor = round(np.mean(ave_doctor), 2)
    max_wait_doctor = round(np.mean(max_doctor), 2)

    print('\n\nAfter {} times of simulation:'.format(sample), file=outfile)
    print("\nThe utilization of nurse is {}%".format(utilization_nurse), file=outfile)
    print("The utilization of doctor is {}%".format(utilization_doctor), file=outfile)
    print('\nThe average and maximum waiting time for nurse are {} minutes and {} minutes'.format(average_nurse, max_wait_nurse), file=outfile)
    print('The average and maximum waiting time for doctor are {} minutes and {} minutes'.format(average_doctor, max_wait_doctor), file=outfile)

    return None


def main():

    clock()

    print('\nWhen there are 8 nurses, 4 doctors, and around 20 patients per hour:', file=outfile)
    for i in [20, 200, 2000, 20000]:
        simulation(8, 4, 20, i)

    print('\nTotal running time is %-1.5ss' % clock())


if __name__ == '__main__':

    with open('Output.txt', 'w') as outfile:
        main()

