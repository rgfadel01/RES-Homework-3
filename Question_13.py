import pypsa

import pandas as pd

#network
n = pypsa.Network()
hours_needed = pd.date_range('2015-01-01T00:00Z','2015-01-01T4:00Z', freq='H')
n.set_snapshots(hours_needed)
n.add("Carrier", "onshorewind")
n.add("Carrier", "solar")

nodes = pd.Series(['DK1','DK2',]).values
neighbors =pd.Series(['DK1','DK2']).values
n.add("Bus",'DK1')
n.add("Bus",'DK2')

#Loads
df_elec = pd.read_csv('electricity_demand_HMWRK3_Q12.csv', sep=';', index_col=0) # in Wh
df_elec.index = pd.to_datetime(df_elec.index) #change index to datatime
print(df_elec['DK1'].head())
print(df_elec['DK2'].head())

n.madd("Load",
        nodes, 
        bus=nodes, 
        p_set=df_elec[nodes])

#Link# Links between neighboring countries
n.add("Link",
     neighbors[0] + ' - ' + neighbors[1],
     bus0=neighbors[0],
     bus1=neighbors[1],
     p_nom_extendable=True, # capacity is optimised
     p_min_pu=-1,
     length=600, # length (in km) between country a and country b
     capital_cost=400*58) # capital cost [EUR/MW/km] * length [km] 

#CF's
df_onshorewind = pd.read_csv('Wind_HMWRK3.csv', sep=';', index_col=0)
df_onshorewind.index = pd.to_datetime(df_onshorewind.index)
df_PV = pd.read_csv('pv_optimal_HMWRK3.csv', sep=';', index_col=0)
df_PV.index = pd.to_datetime(df_PV.index)

CF_wind = df_onshorewind['DK'][[hour.strftime("%Y-%m-%dT%H:%M:%SZ") for hour in n.snapshots]]
CF_pv = df_PV['DK'][[hour.strftime("%Y-%m-%dT%H:%M:%SZ") for hour in n.snapshots]]


def annuity(n,r):
    """Calculate the annuity factor for an asset with lifetime n years and
    discount rate of r, e.g. annuity(20,0.05)*20 = 1.6"""

    if r > 0:
        return r/(1. - 1./(1.+r)**n)
    else:
        return 1/n
capital_cost_onshorewind = annuity(30,0.07)*910000*(1) # in €/MW
capital_cost_PV = annuity(30,0.07)*425000*(1) # in €/MW

#Generators
n.add("Generator",
            "onshorewind",
            bus="DK1",
            p_nom_extendable=True,
            carrier="onshorewind",
            #p_nom_max=1000, # maximum capacity can be limited due to environmental constraints
            capital_cost = capital_cost_onshorewind,
            marginal_cost = 0,
            p_max_pu = CF_wind)
n.add("Generator",
            "PV",
            bus="DK2",
            p_nom_extendable=True,
            carrier="PV",
            #p_nom_max=1000, # maximum capacity can be limited due to environmental constraints
            capital_cost = capital_cost_PV,
            marginal_cost = 0,
            p_max_pu = CF_pv)

n.lopf(n.snapshots, 
             pyomo=False,
             solver_name='gurobi')

#print(network.objective/1000000) #in 10^6 €
print((n.objective/n.loads_t.p.sum())*5/8760) # €/MWh

print (n.generators.p_nom_opt/1000000000) # in GW