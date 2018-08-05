## Title: 
- Emergency Room Waiting Simulation
## Team Member(s): 
- Nanzhu Liu & Qiuyan Guo

## Monte Carlo Simulation Scenario & Purpose:
- This project is to make simulations for the nurses & doctors v.s. patients situation in an emergency room of a hospital, to see the utilization rates of nurses and doctors, and the waiting time of patients, then find the nurses/doctors & patients combination benefiting both the patients (short waiting time) and the hospital (no personnel wasted)
  #### Assumptions:
  - The numbers of nurses and doctors are assigned at any given time, no breaks or shift time waste for these nurses and doctors
  - The the number of patients per hour will be within a given range
  - All of the patients will see a nurse first, 20% of them will leave after seeing the nurse, the rest of them will see a doctor after the nurse
  - The time a nurse / doctor spending with a patient follows the same normal distribution, with the assigned mean time value, sd = 1, min/max = mean -/+ 10
  - All time-related values are in minute(s)
  - Try different sets of given numbers to simulate the situations could be a way to find out what combinations would benefit both the patients and the hospital

## Simulation's variables of uncertainty:
- The main uncertainty is how patients with different purposes arrive randomly and spend uncertain time with nurses/doctors
  #### Random variables:
  - Number of patients per hour
  - The arrival time of each patient per hour
  - Either a patient comes only to see a nurse or to see both a nurse and a doctor
  - The time(minutes) a nurse / doctor spent with a patient

## Hypothesis or hypotheses before running the simulation:
- First, when utilization < 1, patients do not have to wait.
- Second, when utilization > 1, patients must need to wait for nurses or doctors, the higher the utilization rates of both nurses and doctors are, the longer patients tend to wait
- Third, when the mean time a doctor spent with a patient is 30 minutes, to achieve the best nurse/doctor/patient combination, the number of nurses has to be 50% of the number of patients, and the number of doctors has to be the 25% of the number of patients

## Analytical Summary of findings: 
- We have to change the assumptions several times based on the simulation outcomes during the process
- With each set of numbers, the results remain stable after 20000 times of simulations
- First hypothesis is correct
- Second hypothesis goes well with nurses, not doctors; the time that patients wait for nurses is minimal when nurse utilization rate close to 1, then increase along with the rate; while for doctors, the start waiting point is over 1 (around 1.3 - 1.5), the time that patients wait for doctors mostly depends on the time a doctor spends with a patient
- Third hypothesis situation tend to follow a pattern:
    - If rate = (time_spent_with_a_patient) / 60:
    - Nurse_number = (patient_number * rate), which ensures nurse utilization rate close to 1, patients' average waiting time close to 0, and max waiting time around 2 min; and 
    - Doctor_number = (patient_number * rate *（range 0.5 to 0.6)), which ensures minimal doctor personnel waste, patients waiting for doctor time close to 0, and max waiting time less than 6 min
- The results of max waiting time are less concentrated comparing to average waiting time results along with the simulation time



## Instructions on how to use the program:
- Run the Main.py file, which contains the complete program to print both utilization and waiting time calculation results simultaneously (over 30 min for one simulation)
- When calling the simulation function in the main function, the values of the parameters refering to numbers of nurses, doctors, patients, time a nurse/doctor spent with a patient, and running times, could be changed, to get results from different scenarios
  The range of patients number will be (patients-2, patients+2)
- Example_plots.ipynb contains same algorithm, only to show an example of the plots based on one set of people numbers
- Output.txt contains printed results of the similuations of several sets of people numbers currently in the main.py file as examples

## Tasks:
- Time distribution, Utilization calculation - Nanzhu Liu
- Waiting time calculation - Qiuyan Guo
