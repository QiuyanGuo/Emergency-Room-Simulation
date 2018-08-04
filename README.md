## Title: 
- Emergency Room Waiting Simulation
## Team Member(s): 
- Nanzhu Liu & Qiuyan Guo

## Monte Carlo Simulation Scenario & Purpose:
- This project is to make simulations for the nurse & doctor v.s. patients situation in an emergency room of a hospital, to see the utilization rates of nurses and doctors, and the waiting time of patients, then find the nurse/doctor & patient combination benefiting both the patients (short waiting time) and the hospital (no personnel wasted)
  #### Assumptions:
  - The numbers of nurses and doctors are assigned at any given time, no breaks or shift time waste for these nurses and doctors
  - The approximate patient number per hour is assigned, the exact patient number will be within 2 people of the given number
  - All of the patients will see a nurse first, 20% of them will leave after seeing the nurse, the rest of them will also see a doctor after the nurse
  - Time a nurse / doctor spending with a patient follows the same normal distribution, with the assigned mean time value, sd = 1, min/max = mean -/+ 10
  - All time-related values are in minute(s)
  - Try different sets of given numbers to simulate the situations could be a way to find out what combinations would benefit both the patients and the hostipal

## Simulation's variables of uncertainty:
- The main uncertainty is how patients with different purposes arrive randomly and spend uncertain time with nurses/doctors
  #### Random variables:
  - Exact patient numbers in an hour
  - The arrival time of each patient in the hour
  - Either a patient comes only to see a nurse or to see both a nurse and a doctor
  - The time(minutes) a nurse / doctor spent with a patient

## Hypothesis or hypotheses before running the simulation:
- The higher the utilization rates of both nurses and doctors go, the longer patients tend to wait 
- When utilization results > 1, patients must need to wait for nurse or doctor, vice versa
- When mean time spent with a patient is 30 minutes, for a given number of patients in an hour, 1/2 number of nurses and 1/4 number of nurses are needed

## Analytical Summary of findings: 
- We indeed needed to change the assumptions several times based on the simulation outcomes during the process
- With each set of numbers, the results remain stable after 20000 times of simulations
- First hypothesis correct
- Second hypothesis goes well with nurses, not doctors; patients' waiting nurse time is minimal when nurse utilization rate close to 1, then increase along with the rate; while for doctors the start waiting point is over 1 (around 1.3 - 1.5), mostly related to the time spent with a patient
- Third hypothesis situation tend to follow a pattern: 
    - If r = (time_spent_with_a_patient) / 60, then (patient_number * r) number of nurses would be the best choice, which ensures nurse utilization rate close to 1, patients' average waiting time close to 0, and max waiting time around 2 min; and around (patient_number * r * 0.55) number of doctors would be the best choice, which ensures patients waiting for doctor time close to 0, and max waiting time less than 1 min
- Max waiting time results of the simulations are less concentrated comparing to average waiting time results

## Instructions on how to use the program:
- Run the Main.py file, which contains the complete program to print both utilization and waiting time calculation results simultaneously (over 30 min for one simulation)
- When calling the simulation function in the main function, the values of the parameters refering to numbers of nurses, doctors, patients, time a nurse/doctor spent with a patient, and running times, could be changed, to get results from different scenarios
- Example_plots.ipynb contains same algorithm, only to show an example of the plots based on one set of people numbers
- Output.txt contains printed results of the similuations of several sets of people numbers currently in the main.py file as examples

## Tasks:
- Time distribution, Utilization calculation - Nanzhu Liu
- Waiting time calculation - Qiuyan Guo
