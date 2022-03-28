from flask import Flask, redirect, url_for, render_template, request
from flask import Flask, request
import json, pickle
import sys
import time
import PDDL
import pprint
from classes import Object, Action, State, Explanation, Problem




#PDDL Helpers
#Functions to get state at steps
def get_state(step, user=0):
    act_list = problems[user].plan
    i_state = problems[user].initial_state
    if step==-1 or step>len(act_list):
        step = len(act_list)
    plan = Explanation(i_state, act_list)
    i=0
    bad_acts = []
    while i<step:
        bad_acts.append([act_list[i][0].name, act_list[i][1], plan.take_step()])
        i+=1
    # print(bad_acts)
    return plan.current_state

#Function to get precondition flow for a particular step
def get_precondition_flow(step, user=0):
    act_list = problems[user].plan
    if step==0:
        return {}
    [action, parameters] = act_list[step-1]  #using step-1 because first state is initial state, so action (step-1) will happen after state (step)
    grounded_action = action.ground(parameters)
    print(action.name)
    flows={}
    for pre in grounded_action["preconditions"]:
        pred = pre[0]
        objs = pre[1:]
        flow=[]
        for i in range(step):
            #if agent, make false the ones changed in domain/prob

            if domain == 'custom_logistics/agent2.pddl' and user==1 and  pred=='is-hub':
                print(pred, objs, pred=="is-hub")
                flow.append(objs not in states_list[user][i][pred])
                print(flow)
            else:
                flow.append(objs in states_list[user][i][pred])

        flows[str(pre)] = flow
    return flows

def get_goal_state_flow(user=0):
    goal_preconditions = []
    for k,v in problems[user].goal_state.variables.items():
        for preds in v:
            a = [k]
            a.extend(preds)
            goal_preconditions.append(a)
    flows={}
    for pre in goal_preconditions:
        pred = pre[0]
        objs = pre[1:]
        flow=[]
        for i in range(len(states_list[user])-1): #-1 for when states include goal state
            flow.append(objs in states_list[user][i][pred])
        flows[str(pre)] = flow
    return flows

def get_states(user = 0):
    act_list = problems[user].plan
    i_state = problems[user].initial_state
    step = len(act_list)
    plan = Explanation(i_state, act_list)
    i=0
    bad_acts = []
    t_states = []
    for i in range( len(problems[user].plan) + 1):
        t_states.append(get_state(i, user).variables)
    t_states.append(problems[user].goal_state.variables)
    # print(bad_acts)
    return t_states

def get_flows(user=0):
    t_flows=[]
    for i in range( len(problems[user].plan) + 1):
        t_flows.append(get_precondition_flow(i, user))
    t_flows.append(get_goal_state_flow(user))
    return t_flows


#user problem
# scenario_num = 3
# scenario = json.load(open('scenario'+str(scenario_num)+'.json','r'))
viz_type = 'conductor'
viz_type = 'abstraction'
viz_type = 'text'
viz_type = "viz"
domain = 'custom_logistics/agent2.pddl'
problem_file = 'custom_logistics/prob2.pddl'
# viz_type = scenario["viz_type"]
# domain = scenario["domain"]
# problem_file = scenario["problem_file"]
solution_file = []
problem = Problem(domain, problem_file, solution_file)


text_explanation = {"wrong":[],"required":[]}
#Each item in the explanation is formatted as:
#  [ Action name or s/g state, list of ['pred name',[list of objects/parameters]]]
# Example- missing precondition in move airplane(airplane, src, dest) that souxwrce and destination should be hubs:
#       ['move-airplane',[['is-hub',[1]],['is-hub',[2]]]
# Or missing precondition that airplane should be in src
#       ['move-airplane',[['in',[0,1]]]
# Can also have names of objects instead of numbers, but would require different parsing
#
# For wrong information/information to be removed
if domain=='custom_logistics/agent2.pddl':
    text_explanation["required"].append(['move-airplane',[['is-hub',[1]],['is-hub',[2]]]])
if problem_file=='custom_logistics/prob2.pddl':
    text_explanation["wrong"].append(['Initial State',[['in',["package1","location1"]]]])
    text_explanation["required"].append(['Initial State',[['in',["package1","location3"]]]])

#Setting up correct problem
correct_domain = 'custom_logistics/agent.pddl'
correct_problem_file = 'custom_logistics/prob1.pddl'
correct_solution_file = 'custom_logistics/plan.txt'
correct_problem = Problem(correct_domain, correct_problem_file, correct_solution_file)

problems = [problem, correct_problem]
print("Problems: ")
init_states = json.dumps(correct_problem.initial_state.variables)
print(init_states)
states= get_states(0)
correct_states = get_states(1)
states_list = [states, correct_states]

flows = get_flows(0)    #Not very efficient. Multiple variables would be stored repeatedly. Might still be better than storing every possible variable though
correct_flows = get_flows(1)

# print("Correct Flows: ")
# print(correct_flows)
flows_list = [flows, correct_flows]

solutions_list = [solution_file, correct_solution_file]










#FLASK
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/visualization")
def viz():
    return render_template("visualization.html")

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()