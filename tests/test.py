import numpy as np
import random

# TODO Remake the neuron connections and value assigning amk
#   1.  DONE    Inputların ürettiği/sahip olduğu değerleri 0.0 ila 1.0 arasında olmasını sağla.
#   2.  DONE    Neural connectionları oluştur : En fazla 12 connection olabilir. 
#   2.1 DONE    Pay attention to not to connect to neurons multiple times
# * 2.2 Test neural connections.
# * 3.  Calculate Connection values : Connection weight -4.0 to 4.0 * neuron output (Exp. Input neuron output => 0.4 * 3.4 <= Connection weight)
# * 4.  Calculate Internal and Action neuron's recieved values => tanh(sum(inputs)) => -1.0 to 1.0
# ! Note:   Internal Neurons Default value => 1.0

# TODO  Collect similation data for input neurons and arrange them 0.0 to 1.0
# * 1.  Make creatures move using action neurons' outputs

# TODO  Make generation system and upgrade the simulation

# Nöron sınıfı
class Neuron:
    def __init__(self, neuron_type, name):
        self.neuron_type = neuron_type
        self.name = name
        self.value = 0.0
        self.connections = []
        self.recievedConnections = []
        self.totalInputsSum = 0.0
        self.totalInputsCount = len(self.recievedConnections)

    def connect(self, target_neuron, weight):
        self.connections.append((target_neuron, weight))

    def activate(self):
        if self.neuron_type != 'input':  # Input nöronları aktive olmaz
            print("ACTIVATE : ", self.name)
            print("RECIEVED : ", self.recievedConnections)
            total_input = sum(neuron.value * weight for neuron, weight in self.recievedConnections)
            
            self.value = np.tanh(total_input)  # -1.0 ile 1.0 arasında çıktı
            print("VALUE : ", self.value)
            if (self.neuron_type == 'internal') and (self.recievedConnections == []):
                self.value = 1.0

    # Bağlantıları, ağırlıkları ve kendi değerini yazdırmak için bir fonksiyon
    #
    # def print_debug_info(self, output_neurons):
    #    output_connections = [conn for conn in self.connections if conn[0] in output_neurons]
    #    if output_connections:
    #        print(f"Neuron {self.name}: Value = {self.value}")
    #        for target_neuron, weight in output_connections:
    #            print(f"  -> Connected to {target_neuron.name} with weight {weight}")


# Neural Network sınıfı
class NeuralNetwork:
    def __init__(self, input_neurons, internal_neurons, output_neurons):
        # Define Neurons
        self.input_neurons = input_neurons
        self.internal_neurons = internal_neurons
        self.output_neurons = output_neurons
        self.all_neurons = input_neurons + internal_neurons + output_neurons
        self.create_limited_connections()

    def create_limited_connections(self):
        max_total_connections = 12  # Maximum possible connection count
        total_connections = 1
        
        target_connection_count = random.randint(1, 12)

        # ! Default Connection: Atleast one connection with the target of a output neuron has to be connected
        default_connection_output_neuron = np.random.choice(self.output_neurons)
        default_connection_sender_neuron = np.random.choice(self.input_neurons + self.internal_neurons)
        weight = random.uniform(-4.0, 4.0)
        default_connection_sender_neuron.connect(default_connection_output_neuron, weight)

        default_connection_output_neuron.recievedConnections.append((default_connection_sender_neuron, weight))
        default_connection_output_neuron.totalInputsSum += weight * default_connection_sender_neuron.value

        #for i in range(target_connection_count - 1):
            
            #source_neuron = np.random.choice(self.input_neurons + self.internal_neurons)

            #possible_neurons = []

            #if source_neuron.neuron_type == "input":
            #    target_neuron = np.random.choice(self.output_neurons + self.internal_neurons)
            #elif source_neuron.neuron_type == "internal":
            #    combined_except_source = [x for x in (self.output_neurons + self.internal_neurons) if x != source_neuron]
            #    target_neuron = np.random.choice(combined_except_source)
            #weight = random.uniform(-4.0, 4.0)

            ## connect the neurons : 
            #source_neuron.connect(target_neuron, weight)
            #target_neuron.recievedConnections.append((target_neuron, weight))
            #
            ## add the multiplied value to the source
            #target_neuron.totalInputsSum += weight * target_neuron.value
            #total_connections += 1
        a = 0
        while True:
            source_neuron = np.random.choice(self.input_neurons + self.internal_neurons)

            if source_neuron.neuron_type == "input":
                target_neuron = np.random.choice(self.output_neurons + self.internal_neurons)
            elif source_neuron.neuron_type == "internal":
                combined_except_source = [x for x in (self.output_neurons + self.internal_neurons) if x != source_neuron]
                target_neuron = np.random.choice(combined_except_source)
            weight = random.uniform(-4.0, 4.0)

            targetCon = []
            for con in target_neuron.connections:
                targetCon.append(con[0])

            if (source_neuron not in targetCon) and (source_neuron != target_neuron):
                # connect the neurons : 
                print("source neuron name : ", source_neuron.name, source_neuron)
                print("target neuron name : ", target_neuron.name, target_neuron)
                print("target neuron cons : ", targetCon)
                
                source_neuron.connect(target_neuron, weight)
                target_neuron.recievedConnections.append((source_neuron, weight))

                # add the multiplied value to the source
                # ! check the totalInputsSum 
                target_neuron.totalInputsSum += weight * source_neuron.value
                total_connections += 1
                print("\n\n\nCONNECTION  :  ", source_neuron.name, target_neuron.name, "\n\n", source_neuron.connections,"\n\n")
                
            a += 1
            if a == 10: break
            if total_connections == target_connection_count-1: break

        self.total_connections = total_connections

    def set_input_values(self, input_data):
        for neuron in self.input_neurons:
            neuron.value = input_data[neuron.name]  # -1.0 ile 1.0 arasında normalize et

    def feed_forward(self):
        for neuron in self.internal_neurons:
            neuron.activate()
        for neuron in self.output_neurons:
            neuron.activate()

    def get_output_values(self):
        return {neuron.name: neuron.value for neuron in self.output_neurons}

    # Debugging için toplam bağlantı sayısını ve output nöronlarına bağlantıları yazdır
    def print_debug_info(self):
        print(f"Total Connections: {self.total_connections}")
        print("All Neuron Connections:")
        for neuron in self.all_neurons:
            # Old method : 
            # neuron.print_debug_info(self.output_neurons)
            print("NEURON NAME : ", neuron.name)
            print("NEURON TYPE : ", neuron.neuron_type)
            print("NEURON VALUE : ", neuron.value)
            print("NEURON SENDED CONNECTIONS : ")
            for connection in neuron.connections:
                print("Connected to :", connection[0].name, "\nwith the weight of : ", connection[1])
            print("NEURON RECIEVED CONNECTIONS : ")
            for connection in neuron.recievedConnections:
                print("Connected to :", connection[0].name, "\nwith the weight of : ", connection[1])
            print("---------------------------------")

# Agent sınıfı
class Agent:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.last_move_x = 0
        self.last_move_y = 0

        # Input neurons
        input_neurons = [
            Neuron('input', 'Lx'), Neuron('input', 'Ly'), Neuron('input', 'Age'),
            Neuron('input', 'Rnd'), Neuron('input', 'Blr'), Neuron('input', 'Bfd'),
            Neuron('input', 'Plr'), Neuron('input', 'Pfd'), Neuron('input', 'LMy'),
            Neuron('input', 'LMx'), Neuron('input', 'BDy'), Neuron('input', 'BDx'),
            Neuron('input', 'Gen'), Neuron('input', 'BDd'), Neuron('input', 'LPf')
        ]

        # 3 internal neurons
        internal_neurons = [Neuron('internal', f'N{i}') for i in range(3)]

        # assing the default internal neuron value (1.0)
        for internal in internal_neurons:
            internal.value = 1.0

        # Output/Action neurons
        output_neurons = [
            Neuron('output', 'Mfd'), Neuron('output', 'Mrn'), Neuron('output', 'Mrv'),
            Neuron('output', 'MX'), Neuron('output', 'MY')
        ]

        # ! Create Neural Network
        self.network = NeuralNetwork(input_neurons, internal_neurons, output_neurons)

    def update(self, simulation_data):
        self.network.set_input_values(simulation_data)
        self.network.feed_forward()

        # Debugging: Toplam bağlantı sayısını ve output nöronlarına bağlantıları yazdır
        # self.network.print_debug_info()

        output_values = self.network.get_output_values()
        self.move(output_values)


    # OUTPUT NEURONS : 
    #   DONE  Mfd - move forward
    #   DONE  Mrn - move random
    #   DONE  Mrv - move reverse
    #   DONE  MX - move east/west (+/-)
    #   DONE  MY - move north/south (+/-)

    def move(self, output_values):
        if output_values['Mrn'] > 0:
            directions = ['n', 'e', 's', 'w']
            choice = np.random.choice(directions)
            if choice == 'n':
                self.Y += 1
                self.last_move_y += 1
            if choice == 'e':
                self.X = self.X + 1
                self.last_move_x += 1
            if choice == 's':
                self.Y += -1
                self.last_move_y += -1
            if choice == 'w':
                self.X = self.X - 1
                self.last_move_x += -1

        if output_values['Mfd'] > 0:
            self.X = self.X + 1
            self.last_move_x += 1

        if output_values['Mrv'] > 0:
            self.X = self.X - 1
            self.last_move_x += -1

        if output_values['MX'] > 0.3:
            self.X = self.X + 1
            self.last_move_x += 1

        if output_values['MX'] < -0.3:
            self.X = self.X - 1
            self.last_move_x += -1

        if output_values['MY'] > 0.3:
            self.Y += 1
            self.last_move_y += 1

        if output_values['MY'] < -0.3:
            self.Y += -1
            self.last_move_y += -1
    def MovementPossible():
        print("check if new cord in another agent or outsşde of the border")


# Example Similation Data/Values
simulation_data = {
    'Lx': 0.5,
    'Ly': -0.5,
    'Age': 0.3,
    'Rnd': -0.7,
    'Blr': 0.2,
    'Bfd': -0.3,
    'Plr': 0.1,
    'Pfd': -0.4,
    'LMy': 0.0,
    'LMx': 0.0,
    'BDy': 0.6,
    'BDx': -0.6,
    'Gen': 0.8,
    'BDd': -0.2,
    'LPf': 0.4
}

# Agent'ı oluştur ve güncelle
agent = Agent(10, 20)
agent.update(simulation_data)
agent.network.print_debug_info()
