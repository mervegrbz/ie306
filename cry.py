from numpy import random
from scipy import stats
import pandas

# Variable declarations
patient_per_hour = 1
S = 3
Triage_nurse_rate = 0.476190476
p_1 = 0.2
p_2 = 1 - 0.2
K = 5
Healing_in_hospital_rate = 0.213333333
healing_of_stable_rate = 0.16
rejected_critical_patients = 0
time_of_simulation = 0
event_count = 0
last_arrival = 0
# Seed 
random.seed(45) # 2018400186 + 2021400303



nurses = [{'arrival':0,'departure':0,'availability':True} for i in range(0,S)]
nurses_work_times = [0 for i in range(S)]
beds = [{'departure':0,'availability':True}for i in range(0, K)]
queue_nurse = []
waiting_in_queue = []
healing_time = []
healed_patient = 0


def Execute_Arrival(id):
  queue_nurse.append({'id':id,'arrival_time':time_of_simulation,'departure_time':0})
  if check_nurse_availability():
    Execute_Arrival_Nurse()



def Execute_Arrival_Nurse():
  patient = queue_nurse.pop()
  waiting_in_queue.append({'id':id,'arrival_time':patient['arrival_time'],'departure_time':time_of_simulation})
  departure_time = Generate_Nurse_Service_Time() + time_of_simulation
  available_nurse = check_nurse_availability() - 1
  nurses[available_nurse]['departure'] = departure_time
  nurses[available_nurse]['availability'] = False
  nurses_work_times[available_nurse] += departure_time - time_of_simulation 
  event_list.append({'id':patient['id'],'time':departure_time, 'type':'DN'})



def Execute_Departure_Nurse(patient):
  condition = Generate_Condition()
  global nurses
  global rejected_critical_patients
  nurses = [{'departure':nurse['departure'],'availability':time_of_simulation == nurse['departure']} for nurse in nurses]
  if condition == 's':
    departure_from_heal = Generate_Home_Healing_Time('s') + time_of_simulation
    event_list.append({'id':patient,'time':departure_from_heal, 'type':'DH'})
  else:

    if(check_bed_availability()):
      departure_from_heal = Generate_Hospital_Healing_Time() + time_of_simulation
      beds[check_bed_availability()-1]['departure'] = departure_from_heal
      beds[check_bed_availability()-1]['availability'] = False
      event_list.append({ 'id': patient,'time': departure_from_heal,'type': 'DB' })
    else:
      rejected_critical_patients += 1
      departure_from_heal = Generate_Home_Healing_Time('c') + time_of_simulation
      event_list.append({ 'id': patient,'time': departure_from_heal,'type': 'DH' })


def Execute_Departure_HomeCare(patient):
  global healed_patient
  healed_patient+=1
  print('beloo',patient)
  

def Execute_Departure_Bed(patient):
  global beds
  global healed_patient
  healed_patient+=1
  beds = [{'departure':bed['departure'], 'availability':time_of_simulation == bed['departure']} for bed in beds]



def Generate_interarrival():
  return round(random.exponential(scale=float(60)),0) 

def Generate_Nurse_Service_Time():
  return round(random.exponential(scale=float(60/Triage_nurse_rate)),0)

def Generate_Condition():
  number = random.rand()
  return 'c' if number <= p_1  else 's' 

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

#def Arrival():
#   Generate_interarrival()
#  return last_arrival

def Departure_Triage():
  print('beloo')

def Treated_at_Hospital():
  print('beloo')

def Advance_Time(time):
  time_of_simulation = time

def Execute_Event(event):
  print(event)
  time = event['time']
  Advance_Time(time)
  if event['type'] == 'A':
    Execute_Arrival(event['id'])
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
interarrival_list = [ Generate_interarrival() for i in range(0,100)] # Arrival()

event_list = [ ({'id':i+1, "time":value, 'type':'A' }) for i, value in enumerate(interarrival_list) ]
nurse_service_time = [ Generate_Nurse_Service_Time() for i in range(0,100)]
hospital_healing_time = [Generate_Hospital_Healing_Time() for i in range(0,100)]
triage_result = [round(random.rand(),2) for i in range(0,100)]
home_healing_stable = [Generate_Home_Healing_Time('s') for i in range(0,100)]

home_healing_critical = [Generate_Home_Healing_Time('c') for i in range(0,100)]

triage_result_df = pandas.DataFrame(triage_result)
home_healing_critical_df = pandas.DataFrame(home_healing_critical)
home_healing_stable_df = pandas.DataFrame(home_healing_stable)
nurse_service_time_df = pandas.DataFrame(nurse_service_time)
hospital_healing_time_df = pandas.DataFrame(hospital_healing_time)
interarrival_df = pandas.DataFrame(interarrival_list)

triage_result_df.to_csv("triage_1.csv")
home_healing_critical_df.to_csv("home_healing_critical_df1.csv")
home_healing_stable_df.to_csv("home_healing_stable_df1.csv")
nurse_service_time_df.to_csv("nurse_service_time_df1.csv")
hospital_healing_time_df.to_csv("hospital_healing_time_df1.csv")
interarrival_df.to_csv("interarrival_df1.csv")


Time = 0


while healed_patient < 6:
  event_list.sort(key=lambda x: (x['time']))
  event = event_list.pop(0)
  time_of_simulation = event['time']
  Execute_Event(event)
  event_count += 1

      









