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
    def get_state(x):
        if x not in state_dict:
            return ''
        return state_dict[x]
    states = states.apply(lambda x: get_state(x))
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

# Helper functions for completing an experiment
import glob
def complete_experiment(simout_dir):
    outfiles = glob.glob(f'{simout_dir}/*.csv')
    for i, file in enumerate(outfiles):
        df = pd.read_csv(file)
        if i == 0:
            simout = df.copy()
        else:
            simout = simout.append(df)
    simout = simout.rename(columns={'Unnamed: 0' : 'INDEX'})
    simout = simout.set_index(['INDEX'])
    simout = simout.sort_index()
    for i in range(len(soil_subset)):
        if i not in simout.index:
            print(i)
            soil_row = soil_subset.loc[i]
            for col in soil_cols[:-1]:
                soild[col] = soil_row[col]
            latitude, longitude = soil_row['latitude'], soil_row['longitude']
            results = run_wofost(latitude, longitude, cropd, sited, soild, config)
            df_results = pd.DataFrame(results, index=[i])
            df.index.name = 'INDEX'
            simout = simout.append(df_results)
    simout = simout.sort_index()
    return simout

def rerun_wofost(simout):
    # Rerun Wofost for missing weather data
    empty_rows = simout['DVS'].isnull()
    empty_idx = empty_rows.index[empty_rows]
    for i in empty_idx:
        print(i)
        soil_row = soil_subset.loc[i]
        for col in soil_cols[:-1]:
            soild[col] = soil_row[col]
        latitude, longitude = soil_row['latitude'], soil_row['longitude']
        results = run_wofost(latitude, longitude, cropd, sited, soild, config)
        df = pd.DataFrame(results, index=[i])
        df.index.name = 'INDEX'
        simout.loc[i] = df.loc[i]
        #simout = simout.append(df)
    simout.describe() 
