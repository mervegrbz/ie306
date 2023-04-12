from numpy import random
from scipy import stats
import pandas as pd
patient_per_hour = 1
S = 3
Triage_nurse_rate = 0.476190476
p_1 = 0.2
p_2 = 1 - 0.2
K = 5
Healing_in_hospital_rate = 0.213333333
healing_of_stable_rate = 0.16
nurses = [{'arrival':0,'departure':0,'availability':True} for i in range(0,S)]
beds = [{'departure':0,'availability':True}for i in range(0, K)]
rejected_critical_patients = 0
random.seed(45)
nurses_work_times = [0 for i in range(S)]
beds_work_times = [ 0 for i in range(K)] 
duration_homecare = 0
queue_nurse,waiting_in_queue = []
time_of_simulation, event_count, total_healed, total_sick, total_in_hospital, total_homesick = 0
arrived_patient, last_arrived, total_triage_time, total_critical, total_time_healed = 0

def Execute_Arrival(id):
  queue_nurse.append({'id':id,'arrival_time':time_of_simulation,'departure_time':0})
  if check_nurse_availability():
    event_list.append({ 'id': id,'time': time_of_simulation,'type': 'AN' })

def Execute_Arrival_Nurse():
  patient = queue_nurse.pop(0)
  print(time_of_simulation, 'patientim benim',patient)
  waiting_in_queue.append({'id':id,'arrival_time':patient['arrival_time'],'departure_time':time_of_simulation})
  departure_time = Retrieve_Nurse_Service_Time() + time_of_simulation
  available_nurse = check_nurse_availability()-1
  nurses[available_nurse]['departure'] = departure_time
  nurses[available_nurse]['availability'] = False
  nurses_work_times[available_nurse] += departure_time - time_of_simulation 
  event_list.append({'id':patient['id'],'time':departure_time, 'type':'DN'})



def Execute_Departure_Nurse(patient):
  condition = Retrieve_Condition()
  global nurses,total_homesick
  global rejected_critical_patients, total_critical, duration_homecare, total_time_healed
  nurses = [{'departure':nurse['departure'],'availability':time_of_simulation >= nurse['departure']} for nurse in nurses]
  if condition == 's':
    total_homesick += 1
    duration_homecare +=1
    departure_from_heal = Retrieve_Home_Healing_Time('s') + time_of_simulation
    total_time_healed += departure_from_heal - time_of_simulation
    event_list.append({'id':patient,'time':departure_from_heal, 'type':'DH'})
  else:
    total_critical += 1
    if(check_bed_availability()):
      departure_from_heal = Retrieve_Hospital_Healing_Time() + time_of_simulation
      beds_work_times[check_bed_availability()-1] = departure_from_heal - time_of_simulation
      total_time_healed += departure_from_heal - time_of_simulation
      beds[check_bed_availability()-1]['departure'] = departure_from_heal
      beds[check_bed_availability()-1]['availability'] = False
      event_list.append({ 'id': patient,'time': departure_from_heal,'type': 'DB' })
    else:
      total_homesick += 1
      duration_homecare +=1
      rejected_critical_patients += 1
      departure_from_heal = Retrieve_Home_Healing_Time('c') + time_of_simulation
      total_time_healed += departure_from_heal - time_of_simulation
      event_list.append({ 'id': patient,'time': departure_from_heal,'type': 'DH' })
  if (check_nurse_availability()):
    if(len(queue_nurse)):
      event_list.append({ 'id': patien,'time': time_of_simulation,'type': 'AN' })

def Execute_Departure_HomeCare(patient):
  print('beloo',patient)
  global total_healed, total_homesick, duration_homecare
  total_healed += 1
  total_homesick -= 1
  duration_homecare -= 1
  

def Execute_Departure_Bed(patient):
  global beds
  global total_healed
  total_healed+=1
  beds = [{'departure':bed['departure'], 'availability':time_of_simulation >= bed['departure']} for bed in beds]



def Generate_interarrival():
  return round(random.exponential(scale=float(60)),0) 

def Generate_Nurse_Service_Time():
  return round(random.exponential(scale=float(60/Triage_nurse_rate)),0)

def Generate_Condition():
  number = triage_result.pop(0)
  return 's' if number <= p_1  else 'c' 

def Generate_Hospital_Healing_Time():
  return round(random.exponential(scale=float(60/Healing_in_hospital_rate)),0)

def Generate_Home_Healing_Time(type):
  stable = round(random.exponential(scale=float(60/healing_of_stable_rate)),0)
  if type=='s':
    return stable
  else:
    q=random.rand()
    uniform_dist = stats.uniform.ppf(q,loc=1.75,scale=1.25)
    return round(random.exponential(scale=float(60/((1+uniform_dist) * Healing_in_hospital_rate))),0) 

def Arrival():
  global last_arrived, arrived_patient
  arrived_patient+=1
  last_arrived += Retrieve_interarrival()
  return last_arrived

def Retrieve_interarrival():
  return interarrival_list.pop(0)


def Retrieve_Nurse_Service_Time():
  return nurse_service_time.pop(0)

def Retrieve_Condition():
  number = triage_result.pop(0)
  return 's' if number <= p_1  else 'c' 

def Retrieve_Hospital_Healing_Time():
  return hospital_healing_time.pop(0)

def Retrieve_Home_Healing_Time(type):
  if type=='s':
    stable = home_healing_stable.pop(0)
    return stable
  else:
    result = home_healing_critical.pop(0)
    return result 

def Departure_Triage():
  print('beloo')

def Treated_at_Hospital():
  print('beloo')

def Advance_Time(time):
  global time_of_simulation
  time_of_simulation = time

def Execute_Event(event):
  print(event)
  time = event['time']
  Advance_Time(time)
  if event['type'] == 'A':
    Execute_Arrival(event['id'])
  elif event['type'] == 'AN':
    Execute_Arrival_Nurse(event['id'])
  elif event['type'] == 'DN':
    Execute_Departure_Nurse(event['id'])
  elif event['type'] == 'DH':
    Execute_Departure_HomeCare(event['id'])
  elif event['type'] == 'DB':
    Execute_Departure_Bed(event['id'])

def check_nurse_availability():
  for i in range(len(nurses)):
    if nurses[i]['availability']:
      return i+1
  return 0 

def check_bed_availability():
  for i in range(len(beds)):
    if beds[i]['availability']:
      return i+1
  return 0
  
# Arrival : A DepartureNurse: DN ArriveBed: AB DepartureBed : DB DepartureHome: DH
interarrival_list = [ Generate_interarrival() for i in range(0,100)] # Arrival()

event_list = [ ({'id':arrived_patient, "time":Arrival(), 'type':'A'}) for i in range(0,100) ]

nurse_service_time = [ Generate_Nurse_Service_Time() for i in range(0,100)]
hospital_healing_time = [Generate_Hospital_Healing_Time() for i in range(0,100)]
triage_result = [round(random.rand(),2) for i in range(0,100)]
home_healing_stable = [Generate_Home_Healing_Time('s') for i in range(0,100)]
home_healing_critical = [Generate_Home_Healing_Time('c') for i in range(0,100)]
simulation_table = []
total_bed_time = 0
total_nurse_time = 0
average_patient_home = 0
while total_healed < 5:
  duration_homecare = 0 
  earlier_date = time_of_simulation
  event_list.sort(key=lambda x: (x['time'],x['id']),reverse = True)
  event = event_list.pop()
  time_of_simulation = event['time']
  Execute_Event(event)
  total_bed = sum([ 0 if i['availability'] else 1 for i in beds])
  total_bed_time += (time_of_simulation - earlier_date)*total_bed
  total_nurse =  sum([ 0 if i['availability'] else 1 for i in nurses])
  total_nurse_time += total_nurse*(time_of_simulation - earlier_date)
  total_sick = len(queue_nurse) + total_bed + total_nurse + total_homesick 
  simulation_table.append({ 'time':time_of_simulation, 'total Sick':total_sick, 'total in hospital':total_sick - total_homesick, 'total in queue': len(queue_nurse), 'total in bed': total_bed ,'total in nurse':total_nurse, 'total healed': total_healed}| event)
  event_count += 1
  average_patient_home += duration_homecare * (time_of_simulation - earlier_date) 

simulation_table_df = pd.DataFrame(simulation_table)
simulation_table_df.to_csv('Egecanin_gotu.csv')
bed_work = (float(sum(beds_work_times))/K )
nurse_work = (float(sum(nurses_work_times))/S)
kesisim = (bed_work* nurse_work)/ (time_of_simulation)**2
print(kesisim)
joint_prob_empty = (bed_work + nurse_work)/float(time_of_simulation) - kesisim
print(joint_prob_empty)
rejected = rejected_critical_patients/total_critical
print(rejected)
utilization_nurse = nurse_work/float(time_of_simulation)
print(utilization_nurse)
utilization_bed =  bed_work/float(time_of_simulation)
print(utilization_bed)
print(total_bed_time/float(K)) 
print(total_nurse_time/float(S)) 
print(average_patient_home/time_of_simulation)
print(total_time_healed/total_healed)