# main.py

import random
import numpy as np
import pandas as pd
import utilization_waiting as ut
from time import clock

clock()
nurse = 8
doctor = 4
patient = random.randint(15, 25)  # random variable
patient_nurse = int(patient * 0.2)  # patients only to see nurse
patient_nurse_doctor = patient - patient_nurse  # patients to see nurse & doctor

# (mean, sd, min, max) random variables indicating the time(minutes) a patient needs to spent with a nurse/doctor
mean_time = random.randint(25, 35)
sd = 1
min_time = mean_time - 10
max_time = mean_time + 10

# nurse only
total_nurseonly_time = ut.sum_truncnorm(mean_time, sd, min_time, max_time, patient_nurse)
# nurse and doctor
total_nursemix_time = ut.sum_truncnorm(mean_time, sd, min_time, max_time, patient_nurse_doctor)
total_doctor_time = ut.sum_truncnorm(mean_time, sd, min_time, max_time, patient_nurse_doctor)

# utilization
utilization_nurse = ut.rate((total_nurseonly_time + total_nursemix_time), nurse)
utilization_doctor = ut.rate((total_doctor_time), doctor)
print("\nThe utilization of nurse is {}%".format(round(utilization_nurse * 100), 2))
print("The utilization of doctor is {}%".format(round(utilization_doctor * 100), 2))


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

list_nurseonly_number = random.sample(list(range(patient)), patient_nurse)
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


list_mix_patient = [p for p in df_patients[df_patients['Nurse_only'] == False].index]
time_doctor = ut.time_spend(mean_time, sd, min_time, max_time, patient_nurse_doctor)
for i in range(patient_nurse_doctor):
    df_patients.loc[list_mix_patient[i], 'Seeing_doctor'] = time_doctor[i]

for i in range(patient_nurse_doctor):
    if min(arr_doctor) <= df_patients.loc[list_mix_patient[i], 'After_nurse_point']:
        df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] = df_patients.loc[list_mix_patient[i], 'After_nurse_point']
    else:
        df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] = min(arr_doctor)
    df_patients.loc[list_mix_patient[i], 'Waiting_doctor'] = df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] - df_patients.loc[list_mix_patient[i], 'After_nurse_point']
    arr_doctor[np.argmin(arr_doctor)] += df_patients.loc[list_mix_patient[i], 'Seeing_doctor']
    df_patients.loc[list_mix_patient[i], 'After_doctor_point'] = df_patients.loc[list_mix_patient[i], 'Meet_doctor_point'] + df_patients.loc[list_mix_patient[i], 'Seeing_doctor']


average_wait_nurse = round(df_patients['Waiting_nurse'].mean(), 2)
max_wait_nurse = round(df_patients['Waiting_nurse'].max(), 2)
average_wait_doctor = round(df_patients['Waiting_doctor'].sum() / patient_nurse_doctor, 2)
max_wait_doctor = round(df_patients['Waiting_doctor'].max(), 2)

print('\nThe average and maxium waiting time for nurse are {} minutes and {} minutes'.format(average_wait_nurse, max_wait_nurse))
print('The average and maxium waiting time for doctor are {} minutes and {} minutes'.format(average_wait_doctor, max_wait_doctor))

print('\nTotal running time is %-1.5ss' % clock())
