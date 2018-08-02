# main.py

import random
import numpy as np
import pandas as pd
import utilization_waiting as ut
from time import clock


def utilization(mean_time, sd, min_time, max_time, nurse, doctor, patient, p_mix):

    # nurse
    total_nurse_time = ut.sum_truncnorm(mean_time, sd, min_time, max_time, patient)
    # doctor
    total_doctor_time = ut.sum_truncnorm(mean_time, sd, min_time, max_time, p_mix)

    # utilization
    utilization_nurse = ut.rate(total_nurse_time, nurse)
    utilization_doctor = ut.rate(total_doctor_time, doctor)

    return utilization_nurse, utilization_doctor


def wait_time(mean_time, sd, min_time, max_time, nurse, doctor, patient, p_nurseonly, p_mix):

    list_patient = []
    for i in range(patient):
        list_patient.append('patient_{}'.format(i+1))

    total_time = 60
    random_arrival = [random.random() for i in range(patient)]
    sum_arrival = sum(random_arrival)
    arrival_time = [total_time * i / sum_arrival for i in random_arrival]

    df_patients = pd.DataFrame({'Arrival_point': 0, 'Nurse_only': False,
                                'Waiting_nurse': 0, 'Meet_nurse_point': 0,
                                'Seeing_nurse': 0, 'After_nurse_point': 0,
                                'Waiting_doctor': 0, 'Meet_doctor_point': 0,
                                'Seeing_doctor': 0, 'After_doctor_point': 0}, index=list_patient)

    for i in range(patient):
        df_patients.loc[list_patient[i], 'Arrival_point'] += sum(arrival_time[:i])

    list_nurseonly_number = random.sample(list(range(patient)), p_nurseonly)
    for i in list_nurseonly_number:
        df_patients.loc['patient_{}'.format(i + 1), 'Nurse_only'] = True

    arr_nurse = np.zeros(nurse)
    arr_doctor = np.zeros(doctor)

    df_patients['Seeing_nurse'] = ut.time_spend(mean_time, sd, min_time, max_time, patient)

    for i in range(patient):
        if min(arr_nurse) <= df_patients.loc[list_patient[i], 'Arrival_point']:
            df_patients.loc[list_patient[i], 'Meet_nurse_point'] = df_patients.loc[list_patient[i], 'Arrival_point']
        else:
            df_patients.loc[list_patient[i], 'Meet_nurse_point'] = min(arr_nurse)
        df_patients.loc[list_patient[i], 'Waiting_nurse'] = df_patients.loc[list_patient[i], 'Meet_nurse_point'] - df_patients.loc[list_patient[i], 'Arrival_point']
        df_patients.loc[list_patient[i], 'After_nurse_point'] = df_patients.loc[list_patient[i], 'Meet_nurse_point'] + df_patients.loc[list_patient[i], 'Seeing_nurse']

        arr_nurse[np.argmin(arr_nurse)] += df_patients.loc[list_patient[i], 'Seeing_nurse']

    list_nurseonly_patient = [p for p in df_patients[df_patients['Nurse_only'] == True].index]
    for i in range(p_nurseonly):
        df_patients.loc[list_nurseonly_patient[i], 'Waiting_doctor':'After_doctor_point'] = None

    list_mix_patient = [p for p in df_patients[df_patients['Nurse_only'] == False].index]
    time_doctor = ut.time_spend(mean_time, sd, min_time, max_time, p_mix)
    for i in range(p_mix):
        df_patients.loc[list_mix_patient[i], 'Seeing_doctor'] = time_doctor[i]

    for i in range(p_mix):
        if min(arr_doctor) <= df_patients.loc[list_mix_patient[i], 'After_nurse_point']:
            df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] = df_patients.loc[list_mix_patient[i], 'After_nurse_point']
        else:
            df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] = min(arr_doctor)
        df_patients.loc[list_mix_patient[i], 'Waiting_doctor'] = df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] - df_patients.loc[list_mix_patient[i], 'After_nurse_point']
        arr_doctor[np.argmin(arr_doctor)] += df_patients.loc[list_mix_patient[i], 'Seeing_doctor']
        df_patients.loc[list_mix_patient[i], 'After_doctor_point'] = df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] + df_patients.loc[list_mix_patient[i], 'Seeing_doctor']

    average_wait_nurse = round(df_patients['Waiting_nurse'].mean(), 2)
    max_wait_nurse = round(df_patients['Waiting_nurse'].max(), 2)
    average_wait_doctor = round(df_patients['Waiting_doctor'].sum() / p_mix, 2)
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

    print('\nWhen there are 8 nurses, 4 doctors, and around 20 patients per hour', file=outfile)
    for i in [20, 200]:
        simulation(8, 4, 20, i)

    print('\nTotal running time is %-1.5ss' % clock())


if __name__ == '__main__':

    with open('Output.txt', 'w') as outfile:
        main()

