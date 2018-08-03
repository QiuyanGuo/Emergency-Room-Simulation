### 590PR Final_Project (Nanzhu & Qiuyan)

### This project is to make simulations for the nurse & doctor v.s. patients situation in an emergency room of a hospital. The goal is to see the utilization of nurses and doctors, and the waiting time of patients.

### Assumptions:
- The numbers of nurses and doctors are assigned at any given time, no breaks or shift time waste for these nurses and doctors
- The approximate patient number per hour is assigned, the exact patient number will be within 5 people of the given number
- All of the patients will see a nurse first, 20% of them will leave after seeing the nurse, the rest of them will also see a doctor after the nurse
- Time spending with a nurse and a doctor both follow the same normal distribution
- When utilization results > 1, the possibility of patients waiting is quite large
- All time-related values are in minutes

### Random variables:
- Exact patient numbers in an hour
- The arrival time point of each patient in the hour
- Either a patient comes only to see a nurse or to see both a nurse and a doctor
- The time spending with a nurse and a doctor of a patient

### Files:
- Main.py: Complete program with utilization and waiting time calculations
- Example_plots: Same algorithm, only showing the plots based on one set of people numbers
- Output.txt: Printed results of the similuations of several sets of people numbers

### Findings:
- We did need to change the assumptions several times based on the simulation outcomes during the process
- With each set of numbers, the results remain stable after 20000 times of simulations
- After analyzing the output data, we found:
  - When utilization results > 1, the possibility of patients waiting tend to be- quite large

### Tasks:
- Time distribution, Utilization calculation - Nanzhu Liu
- Waiting time calculation - Qiuyan Guo
