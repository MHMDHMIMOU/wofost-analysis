def return_apr_dict(action):
    if action=="irrigate":
        a={'event_signal': 'irrigate',
     'name': 'Irrigation application table',
     'comment': 'All irrigation amounts in cm',}
        b={'amount': 10,
    'efficiency': 0.7}
    if action=="fertilize":
        a= {'event_signal': 'apply_npk',
      'name': 'Timed N/P/K application table',
      'comment': 'All fertilizer amounts in kg/ha',}
        b={'N_amount': 15,
         'P_amount': 15,
         'K_amount': 15,
         'N_recovery': 0.7,
         'P_recovery': 0.7,
         'K_recovery': 0.7}
    return a, b

def generate_action_dict(action, prob_iri, std, tot_days, seed, cost=0):
    random.seed(seed)
    dicton, b = return_apr_dict(action)
    i=0
    flag=0
    totcost=0
    while i<=tot_days:
        if random.random()<=prob_iri:
            if "events_table" not in dicton: dicton["events_table"]=[]
            dicton["events_table"].append({std+datetime.timedelta(i): b})
            flag=1
            totcost+=cost
        i+=1
    if flag==1: return dicton, totcost
    else: return None, totcost

def gen_agromanager(base, dicton, seed, costs): 
    aux=deepcopy(base)
    if len(aux)>1: print(7/0)
    if len(aux[0])>1: print(8/0)
    sd=list(aux[0].keys())[0]
    aux[0][sd]['TimedEvents']=[]
    tot_days=(aux[0][sd]["CropCalendar"]["crop_end_date"]-sd).days
    total_cost=0
    for a, b in dicton.items():
        res, totcostaction=generate_action_dict(a, b, sd, tot_days, seed, cost=costs[a])
        total_cost+=totcostaction
        if res!=None: 
            aux[0][sd]['TimedEvents'].append(res)
    return aux, total_cost    
