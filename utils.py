def us_state_abbrev(states):
    state_dict = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
    }
    states = states.str.title()
    states = states.apply(lambda x: state_dict[x])
    return states

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
