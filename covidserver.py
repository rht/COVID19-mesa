# Santiago Nunez-Corrales and Eric Jakobsson
# Illinois Informatics and Molecular and Cell Biology
# University of Illinois at Urbana-Champaign
# {nunezco,jake}@illinois.edu

# A simple tunable model for COVID-19 response
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from covidmodel import CovidModel
from covidmodel import Stage
from covidmodel import AgeGroup
from covidmodel import SexGroup
from covidmodel import ValueGroup

# Specific model data

# Observed distribution of mortality rate per age
cr_age_mortality = {
    AgeGroup.C80toXX: 0.148,
    AgeGroup.C70to79: 0.08,
    AgeGroup.C60to69: 0.036,
    AgeGroup.C50to59: 0.013,
    AgeGroup.C40to49: 0.004,
    AgeGroup.C30to39: 0.002,
    AgeGroup.C20to29: 0.002,
    AgeGroup.C10to19: 0.002,
    AgeGroup.C00to09: 0.0
}

# Observed distribution of mortality rage per sex
cr_sex_mortality = {
    SexGroup.MALE: 0.62,
    SexGroup.FEMALE: 0.38
}

cr_age_distribution = {
    AgeGroup.C80toXX: 0.023,
    AgeGroup.C70to79: 0.03,
    AgeGroup.C60to69: 0.078,
    AgeGroup.C50to59: 0.109,
    AgeGroup.C40to49: 0.128,
    AgeGroup.C30to39: 0.169,
    AgeGroup.C20to29: 0.169,
    AgeGroup.C10to19: 0.148,
    AgeGroup.C00to09: 0.146
}

# Observed distribution of mortality rage per sex
cr_sex_distribution = {
    SexGroup.MALE: 0.496,
    SexGroup.FEMALE: 0.504
}

# Value distribution per stage per interaction (micro vs macroeconomics)
cr_value_distibution = {
    ValueGroup.PRIVATE: {
        Stage.SUSCEPTIBLE: 1.0,
        Stage.EXPOSED: 1.0,
        Stage.SYMPDETECTED: -0.2,
        Stage.ASYMPTOMATIC: 1.0,
        Stage.ASYMPDETECTED: -0.2,
        Stage.SEVERE: -5.0,
        Stage.RECOVERED: 0.8,
        Stage.DECEASED: 0
    },
    ValueGroup.PUBLIC: {
        Stage.SUSCEPTIBLE: 10.0,
        Stage.EXPOSED: 10.0,
        Stage.SYMPDETECTED: -5.0,
        Stage.ASYMPTOMATIC: 10.0,
        Stage.ASYMPDETECTED: -1.0,
        Stage.SEVERE: -30.0,
        Stage.RECOVERED: 5,
        Stage.DECEASED: -5
    }
}

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    if agent.stage == Stage.SUSCEPTIBLE:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
    elif agent.stage == Stage.EXPOSED:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif agent.stage == Stage.ASYMPTOMATIC:
        portrayal["Color"] = "brown"
        portrayal["Layer"] = 0
    elif agent.stage == Stage.SYMPDETECTED:
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
    elif agent.stage == Stage.ASYMPDETECTED:
        portrayal["Color"] = "cyan"
        portrayal["Layer"] = 0
    elif agent.stage == Stage.SEVERE:
        portrayal["Color"] = "magenta"
        portrayal["Layer"] = 0
    elif agent.stage == Stage.RECOVERED:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    elif agent.stage == Stage.DECEASED:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
    elif agent.locked:
        portrayal["Color"] = "gray"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "gray"
        portrayal["Layer"] = 0

    return portrayal

grid = CanvasGrid(agent_portrayal, 30, 30, 400, 400)

chart = ChartModule([{"Label": "Susceptible",
                      "Color": "Blue"},
                      {"Label": "Incubating",
                      "Color": "Red"},
                      {"Label": "Asymptomatic",
                      "Color": "Brown"},
                      {"Label": "SymptQuarantined",
                      "Color": "Yellow"},
                      {"Label": "AsymptQuarantined",
                      "Color": "Cyan"},
                      {"Label": "Recovered",
                      "Color": "Green"},
                      {"Label": "Severe",
                      "Color": "Magenta"},
                      {"Label": "Deceased",
                      "Color": "Black"},
                      {"Label": "Isolated",
                      "Color": "Gray"},
                      ],
                    data_collector_name='datacollector')

chart_personal_value = ChartModule([{"Label": "CummulPrivValue",
                      "Color": "Black"}
                      ],
                    data_collector_name='datacollector'
)

chart_public_value = ChartModule([
                      {"Label": "CummulPublValue",
                      "Color": "Red"},
                      {"Label": "CummulTestCost",
                      "Color": "Green"}
                      ],
                    data_collector_name='datacollector'
)

chart_epidemiology = ChartModule([
                      {"Label": "Rt",
                      "Color": "Blue"},
                      #{"Label": "CummulTestCost",
                      #"Color": "Green"}
                      ],
                    data_collector_name='datacollector'
)

chart_employment = ChartModule([
                      {"Label": "Employed",
                      "Color": "Blue"},
                      {"Label": "Unemployed",
                      "Color": "Red"}
                      ],
                    data_collector_name='datacollector'
)

model_params = {
    "num_agents": 200,
    "width": 30,
    "height": 30,
    "age_mortality": cr_age_mortality,
    "sex_mortality": cr_sex_mortality,
    "age_distribution": cr_age_distribution,
    "sex_distribution": cr_sex_distribution,
    "prop_initial_infected": UserSettableParameter("slider", "Proportion of initially infected", 0.001, 0.0, 0.1
    , 0.001),
    "avg_incubation_time": UserSettableParameter("slider", "Average incubation time", 5, 2, 24, 1),
    "avg_recovery_time": UserSettableParameter("slider", "Average recovery time", 15, 15, 30, 1),
    "proportion_asymptomatic": UserSettableParameter("slider", "Proportion of asymptomatics", 0.2, 0.0, 1.0, 0.05),
    "proportion_severe": UserSettableParameter("slider", "Proportion of severe cases", 0.13, 0.0, 0.20, 0.01),
    "prob_contagion": UserSettableParameter("slider", "Probability of contagion", 0.03, 0.0, 0.1, 0.005),
    "proportion_isolated": UserSettableParameter("slider", "Proportion isolated", 0.0, 0.0, 1.0, 0.05),
    "day_start_isolation": UserSettableParameter("slider", "Isolation policy start (days) ", 365, 0, 365, 2),
    "days_isolation_lasts": UserSettableParameter("slider", "Duration of isolation policy ", 365, 0, 365, 2),
    "prob_isolation_effective": UserSettableParameter("slider", "Isolation effectiveness", 1.0, 0.0, 1.0, 0.05),
    "social_distance": UserSettableParameter("slider", "Social distance (meters)", 1.8, 0.0, 2.5, 0.1),
    "day_distancing_start": UserSettableParameter("slider", "Social distancing policy start (days) ", 365, 0, 365, 2),
    "days_distancing_lasts": UserSettableParameter("slider", "Duration of social distancing policy ", 365, 0, 365, 5),
    "proportion_detected": UserSettableParameter("slider", "Proportion of detected cases", 0.1, 0.0, 1.0, 0.05),
    "day_testing_start": UserSettableParameter("slider", "Generalized testing policy start (days) ", 365, 0, 365, 2),
    "days_testing_lasts": UserSettableParameter("slider", "Duration of generalized testing policy ", 365, 0, 365, 2),
    "stage_value_matrix": cr_value_distibution,
    "test_cost": 200,
    "alpha_private": UserSettableParameter("slider", "Personal value amplifier", 1.0, 0.0, 2.0, 0.1),
    "alpha_public": UserSettableParameter("slider", "Public value amplifier", 1.0, 0.0, 2.0, 0.1),
}

server = ModularServer(CovidModel,
                       [grid, chart_epidemiology],
                       #[chart_personal_value, chart_public_value],
                       "COVID-19 epidemiological and economic model",
                       model_params
                       )

server.port = 8521 # The default
server.launch()