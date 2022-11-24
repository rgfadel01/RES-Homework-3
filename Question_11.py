import pypsa
import pandas as pd
#Question 11
network = pypsa.Network()
hours_needed = pd.date_range('2015-01-01T00:00Z','2015-01-01T4:00Z', freq='H')
network.set_snapshots(hours_needed)

network.add("Bus","electricity bus")

print(network.snapshots)


# load electricity demand data
df_elec = pd.read_csv('electricity_demand_HMWRK3.csv', sep=';', index_col=0) # in Wh
df_elec.index = pd.to_datetime(df_elec.index) #change index to datatime
print(df_elec['DK'].head())

# add load to the bus
network.add("Load",
            "load", 
            bus="electricity bus", 
            p_set=df_elec['DK'])

print (network.loads_t.p_set)
r=0.07
n=30


def annuity(n,r):
    """Calculate the annuity factor for an asset with lifetime n years and
    discount rate of r, e.g. annuity(20,0.05)*20 = 1.6"""

    if r > 0:
        return r/(1. - 1./(1.+r)**n)
    else:
        return 1/n

network.add("Carrier", "PV")

# add solar PV generator
df_PV = pd.read_csv('pv_optimal_HMWRK3.csv', sep=';', index_col=0)
df_PV.index = pd.to_datetime(df_PV.index)
CF_pv = df_PV['DK'][[hour.strftime("%Y-%m-%dT%H:%M:%SZ") for hour in network.snapshots]]
capital_cost_PV = annuity(30,0.07)*425000*(1) # in €/MW
network.add("Generator",
            "PV",
            bus="electricity bus",
            p_nom_extendable=True,
            carrier="PV",
            #p_nom_max=1000, # maximum capacity can be limited due to environmental constraints
            capital_cost = capital_cost_PV,
            marginal_cost = 0,
            p_max_pu = CF_pv)
print (network.generators_t.p_max_pu)
network.lopf(network.snapshots, 
             pyomo=False,
             solver_name='gurobi')
#print(network.objective/1000000) #in 10^6 €
print((network.objective/network.loads_t.p.sum())*5/8760) # €/MWh

print (network.generators.p_nom_opt/1000000) # in MW
