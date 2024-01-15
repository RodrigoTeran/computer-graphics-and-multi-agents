import agentpy as ap
import numpy as np
# Visualization
import seaborn as sns

def gini(x):

    """ Calculate Gini Coefficient """
    # By Warren Weckesser https://stackoverflow.com/a/39513799

    x = np.array(x)
    mad = np.abs(np.subtract.outer(x, x)).mean()  # Mean absolute difference
    rmad = mad / np.mean(x)  # Relative mean absolute difference
    return 0.5 * rmad

class WealthAgent(ap.Agent):    
    def setup(self):
        self.wealth = 1

    def step(self, e):
        self.action(self.next(self.see(e)))

    def see(self, e):
        return e.random()
    
    def next(self, p):
        if self.wealth > 0: return p
        return self

    def action(self, i):
        self.wealth -= 1
        i.wealth += 1

    def wealth_transfer(self):
        if self.wealth <= 0: return # We can't transfer
        
        partner = self.model.agents.random()
        partner.wealth += 1
        self.wealth -= 1
        

class WealthModel(ap.Model):
    def setup(self):
        self.agents = ap.AgentList(self, self.p.agents, WealthAgent)

    def step(self):
        self.agents.step(self.agents)

    def update(self):
        self.record('Gini Coefficient', gini(self.agents.wealth))

    def end(self):
        self.agents.record('wealth')


parameters = {
    'agents': 100,
    'steps': 1000,
    'seed': 7
}

model = WealthModel(parameters)
results = model.run()

results.info
results.variables.WealthModel.head()

data = results.variables.WealthModel
data.plot()

sns.histplot(data=results.variables.WealthAgent, binwidth=1)
