"""CLASSES"""
#See example on wikipedia PDDL page
# class Predicate():
#     #creates instance of a predicate. For example, to create a room called 'A', just pass 'room' as type. Cannot instantiate a type, just a member of the type.
#     def __init__(self, ptype, num_inputs, variables, value=True):
#         #ptype = string. Example - room. (Can an object have more than one type? Think)
#         self.num_inputs = num_inputs
#         self.type = ptype
#         self.value = True
#         self.variables = variables
import copy
import PDDL
class Object():
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    # def add_properties(self, )

class Action():
    #preconditions (values of predicates) and add and delete effects (effects)
    #add timestep parameter to predicates or action?
    def __init__(self, preconditions, add_effects, remove_effects, name, num_params = None):
        # self.parameters = parameters            #list of objects required by the action (variable names?)
        self.preconditions = preconditions    #preconditions might look something like [['room',[0]], ['ball', [1]], ['at', [0,1]]] Assuming all preconditions are necessary
        self.add_effects = add_effects                  #effects would be similar
        self.remove_effects = remove_effects
        self.name = name
        self.num_params = num_params

        """
        Even if a predicate uses a single variable, pass it as a list. 
        Format:
            list( predicate_name, list(index of items for predicate))
            [['room',[0]], ['ball', [1]], ['at', [0,1]]]
            0 and 1 being the 0th and 1st object passed to the Action
        """
    def print(self, params):
        op= "action: " + self.name + \
        "\n parameters: " + str(params) + "\n preconditions: \n\t"
        for pred,var in self.preconditions:
            op+=str(pred) +"("
            for i in var:
                op+=str(params[i])+", "
            op=op[:-2]+") \n\t"
        
        op+="\n add effects: \n\t"
        for pred,var in self.add_effects:
            op+=str(pred) +"("
            for i in var:
                op+=str(params[i])+", "
            op=op[:-2]+") \n\t"

        op+="\n remove effects: \n\t"
        for pred,var in self.remove_effects:
            op+=str(pred) +"("
            for i in var:
                op+=str(params[i])+", "
            op=op[:-2]+") \n\t"
        return op
    
    def print2(self, params):
        op= "--Action--\n" + self.name + \
        "\n\n--Parameters--\n" + str(params) + "\n \n--Preconditions--\n"
        for pred,var in self.preconditions:
            op+=str(pred) +"("
            for i in var:
                op+=str(params[i])+", "
            op=op[:-2]+") \n"
        
        op+="\n--Add effects--\n"
        for pred,var in self.add_effects:
            op+=str(pred) +"("
            for i in var:
                op+=str(params[i])+", "
            op=op[:-2]+") \n"

        op+="\n--Remove effects--\n"
        for pred,var in self.remove_effects:
            op+=str(pred) +"("
            for i in var:
                op+=str(params[i])+", "
            op=op[:-2]+") \n"
        return op

    def ground(self, params):
        #return a tuple for preconditions, effects after replacing the variable with given parameter.
        op = {}
        # op = {self.name: self}
        op["preconditions"] = []

        for pred,var in self.preconditions:
            p = [pred]
            for i in var:
                p.append(params[i])
            op["preconditions"].append(p)
        
        op["add_effects"] = []
        for pred,var in self.add_effects:
            p = [pred]
            for i in var:
                p.append(params[i])
            op["add_effects"].append(p)
        
        op["del_effects"] = []
        for pred,var in self.remove_effects:
            # p = ['!',pred] #specific for conductor. Needed?
            p = [pred]
            for i in var:
                p.append(params[i])
            op["del_effects"].append(p)

        return op

    def perform(self, objects, state):
        unsatisfied = []
        flag = 0
        for predicate, var in self.preconditions:
            if state.checkPredicate(predicate, [objects[i] for i in var]) == False:
                flag = 1
                unsatisfied.append([predicate, [objects[i] for i in var]])
        if flag:
            print("preconditions not satisfied for action {}({}): ".format(self.name, objects), unsatisfied)
            return unsatisfied

        for predicate, var in self.add_effects:
            state.addPredicate(predicate, [objects[i] for i in var])

        for predicate, var in self.remove_effects:
            state.removePredicate(predicate, [objects[i] for i in var])
        
        return None
        
        
        


class State():
    #collection of predicates. Stored as a dictionary by predicate type. example {'ball': [[a],[b],[c]]} implies a,b and c are balls
    
    #can this handle facts like "Water_is_cooked"= True #ADD add_facts() METHOD  # Added '' predicate. Should take care of this
    
    def __init__(self, predicate_list):
        #sort out naming convention between variables, objects, predicates and fluents
        self.variables = {}
        for p in predicate_list:
            self.variables[p] = []
    
    def addPredicate(self, predicate, objects):
        if type(objects) != list:
            objects = [objects]
        self.variables[predicate].append(objects)

    def removePredicate(self, predicate, objects):
        if type(objects) != list:
            objects = [objects]
        self.variables[predicate].remove(objects)
    
    def checkPredicate(self, predicate, objects):
        if type(objects) != list:
            objects = [objects]
        if objects in self.variables[predicate]:
            return True
        else:
            return False

    def print(self):
        return self.variables

class Explanation():
    #Same as a plan. A series of actions and an initial state. Performing these actions starting from the initial state leads to the goal state
    def __init__(self, initial_state, actions):
        self.initial_state = initial_state
        self.actions = actions
        self.current_state = copy.deepcopy(initial_state)
        self.step = 0
    
    def take_step(self):
        action,objects = self.actions[self.step]
        unsatisfied = action.perform(objects, self.current_state)
        if 1:#not unsatisfied: #always, for now
            self.step+=1
        return unsatisfied

class Problem():
    #Container for one full problem including domain, goal, solution, problem
    def __init__(self, domain, problem, solution_file):
        self.domain = domain
        self.problem = problem
        self.solution_file = solution_file
        self.parse_problem()
        #Add step here to 
        self.generate_plan()
    
    def parse_problem(self):
        #Parsing
        parser = PDDL.PDDL_Parser()
        parser.parse_domain(self.domain)
        parser.parse_problem(self.problem)
        self.parser = parser

        #saving predicates
        predicates = list(parser.predicates.keys())
        predicates.append('')

        #initialize state
        self.initial_state = State(predicates)
        for s in parser.state:
            self.initial_state.addPredicate(s[0],s[1:])
        
        #initialize goal state
        self.goal_state = State(predicates)
        for s in parser.positive_goals:
            self.goal_state.addPredicate(s[0],s[1:])
        
        #initialize actions
        actions = {}
        for action in parser.actions:
            name = action.name
            p = action.parameters
            param = {}
            for i in range(len(p)):
                param[p[i][0]] = i
            
            prec = action.positive_preconditions
            preconditions=[]
            for item in prec:
                for i in range(1,len(item)):
                    item[i] = param[item[i]]
                preconditions.append([item[0],item[1:]])
            
            adde = action.add_effects
            add_effects=[]
            for item in adde:
                for i in range(1,len(item)):
                    item[i] = param[item[i]]
                add_effects.append([item[0],item[1:]])
            
            dele = action.del_effects
            del_effects=[]
            for item in dele:
                for i in range(1,len(item)):
                    item[i] = param[item[i]]
                del_effects.append([item[0],item[1:]])
            
            actions[name] = Action(preconditions, add_effects, del_effects, name, num_params = p)
        self.actions = actions

    def generate_plan(self):
        plan = []#plan #solution from planner
        if type(self.solution_file) == str:
            with open(self.solution_file) as answers:
                for line in answers:
                    # l= line[1:-2]
                    l = line.split('(')[1].split(')')[0]
                    a = l.split()
                    plan.append([self.actions[a[0]], a[1:]])
        else:
            for  act in self.solution_file:
                a = list(act)
                plan.append([self.actions[a[0]],a[1:]])
        self.plan = plan