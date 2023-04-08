from numpy import random
from scipy import stats

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

# Seed 
random.seed(45) # 2018400186 + 2021400303




nurses = [{'arrival':0,'departure':0,'availability':True} for i in range(0,S)]
nurses_work_times = [0 for i in range(S)]
beds = [{'departure':0,'availability':True}for i in range(0, K)]
queue_nurse = []
waiting_in_queue = []
healing_time = []



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
  print('beloo',patient)
  

def Execute_Departure_Bed(patient):
  global beds
  beds = [{'departure':bed['departure'], 'availability':time_of_simulation == bed['departure']} for bed in beds]



def Generate_interarrival():
  return random.exponential(scale=float(60)) * 60

def Generate_Nurse_Service_Time():
  return random.exponential(scale=Triage_nurse_rate) * 60

def Generate_Condition():
  number = random.rand()
  return 'c' if number <= p_1  else 's' 

def Generate_Hospital_Healing_Time():
  return random.exponential(scale=Healing_in_hospital_rate) * 60

def Generate_Home_Healing_Time(type):
  stable = random.exponential(scale=healing_of_stable_rate) * 60
  if type=='s':
    return stable
  else:
    q=random.rand()
    result=stats.norm.ppf(q,loc=1.75,scale=1.25)
    return result*60 + stable

def Arrival():
  return time_of_simulation + Generate_interarrival()

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
  
# Arrival : A DepartureNurse: DN ArriveBed: AB DepartureBed : DB DepartureHome: DH
interarrival_list = [ Generate_interarrival() for i in range(0,100)]
interarrival_list.sort()
event_list = [ ({'id':i+1, "time":value, 'type':'A' }) for i, value in enumerate(interarrival_list) ]



Time = 0


while event_count < 100:
  event_list.sort(key=lambda x: (x['time']))
  event = event_list.pop(0)
  time_of_simulation = event['time']
  Execute_Event(event)
  event_count += 1

      









