# main.py

import random
import utilization as ut
from time import clock

clock()
nurse = 12
doctor = 10
patient = random.randint(10,25)  #random variable
patient_nurse = int(patient * 0.15)  # patient to see nurse
patient_doctor = int(patient * 0.5)  # patient to see doctor
patient_nurse_doctor = patient - patient_nurse - patient_doctor  # patient to see nurse&doctor

# (mean, sd, min, max)can be changed or give different value with different situation below
mean = 30
sd = 1
min = 20
max = 40

#nurse only
total_nurseonly_time = ut.sum_truncnorm(mean,sd,min,max,patient_nurse)
#doctor only
total_doctoronly_time = ut.sum_truncnorm(mean,sd, min, max, patient_doctor)
#nurse and doctor
total_nursemix_time = ut.sum_truncnorm(mean,sd,min,max,patient_nurse_doctor)
total_doctormix_time = ut.sum_truncnorm(mean,sd,min,max,patient_nurse_doctor)

#utilization
utilization_nurse = ut.rate((total_nurseonly_time + total_nursemix_time),nurse)
utilization_doctor = ut.rate((total_doctoronly_time + total_doctormix_time),doctor)
print("The utilization of nurse is:",utilization_nurse)
print("The utilization of doctor is:",utilization_doctor)

print('total running time is %-1.5ss' % clock())
