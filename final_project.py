import turtle
import random
import math
import time

'''
Features:
1. HeatSource: lightness is changing periodilly, and the brighter the heatsource, the faster the turtles moves towards the heatsource.
2. FoodSource: each food can be consumed by turtles, and once they are touched by turtles, that foodsource disappears. Once all foodsources
have be consumed, turtles can't find other things to eat, and they will wait until die.
3. Turtle: turtles have two inner states. 
    First one is temperature, which starts at 30 degrees. Temperature is dropping by 0.01 every move, and once it drop to 0, the turtle dies.
If the turtle get to the heatsource, temperature will be reset to 30 again.
    Second one is hunger, which is originally set to 0. Hunger is increasing by 0.01 every move, and once it get to 30, the turtle dies. If 
the turtle get to the foodsource, hunger will be reset to 0.
    The turtles decide to go to whether heatsource or foodsource based on which one is losing more. If loss_food is larger than loss_heat, 
turtle will go to foodsource first.
'''

class HeatSource(turtle.Turtle):

    def __init__(self, lightness):
        turtle.Turtle.__init__(self, visible = False)
        self.shape('sun.gif')
        self.penup()
        self.color(255, 190, 60)
        self.goto(random.randint(-200, 200), random.randint(-200, 200))
        self.lightness = lightness
        self.showturtle()

    def lightness_change(self, lightness):
        self.lightness = math.sin(self.lightness)
        return self.lightness
    ### the heat source lightness is changing by a sin function, the brighter the source is, the quicker the turtle moves toward that heat source


class FoodSource(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__(self, visible = False)
        self.shape('food.gif')
        self.penup()
        self.goto(random.randint(-200, 200), random.randint(-200, 200))
        self.showturtle()
        self.quantity = 1
    ### the food source will disappear once they have been touched by turtles.

    def count_food(self):
        self.quantity -= 1
    ### when the food source is touched by the turtles, the count decrease by 1



class Vehicle2(turtle.Turtle):

    def __init__(self, input_heat_list, input_food_list, vehicle_id, vehicle_type, temperature, hunger):
        turtle.Turtle.__init__(self, visible = False)
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.input_heat_list = input_heat_list
        self.input_food_list = input_food_list
        self.temperature = temperature
        self.hunger = hunger
        self.create_vehicle()
        self.speed_parameters = [20, 0.2, 6]
        self.turn_parameters = [20]
        self.moves = 0
        

    def create_vehicle(self):
        self.shape('turtle')
        self.turtlesize(1)
        self.penup()
        if self.vehicle_type == 'crossed':
            self.color(random.randint(0, 150), random.randint(0, 150), 255)
            # blue (moves away from heatsource)
        else:
            self.color(255, random.randint(0, 150), random.randint(0, 150))
            # red
        self.goto(random.randint(-290, 290), random.randint(-290, 290))
        self.right(random.randint(0, 360))
        self.pendown()
        self.showturtle()
        

    def evaluate_temperature(self):
        if -0.1 >= self.temperature <= 0:
            self.hideturtle()
            self.penup()
            print("disappear")
    ### when the temperature of the turtle drop to within 0 and -0.1, the turtle disappear (die)
        else:
            self.temperature = self.temperature - 0.01
    ### turtle's original temperature is 100, and will be decreasing by 0.01 each move.

    def evaluate_hunger(self):
        if self.hunger >= 30 and self.hunger <= 30.1:
            self.hideturtle()
            self.penup()
            print("disappear")
            return self.hunger
    ### when the hunger reaches within 100 and 100.1, the turtle disappear.
        else:
            self.hunger = self.hunger + 0.01
            return self.hunger
    ### turtle's original hunger is 0, and it will be increasing by 0.01 for each move.

    def get_heat_input_information(self, position):
        input_heat_distance = self.distance(position)
        input_heat_angle = self.heading() - self.towards(position)
        return input_heat_distance, input_heat_angle

    def get_food_input_information(self, position):
        input_food_distance = self.distance(position)
        input_food_angle = self.heading() - self.towards(position)
        return input_food_distance, input_food_angle
### get input informaiton for heat and food seperately

    def get_heat_sensor_distances(self, distance, angle):
        sin_angle = math.sin(math.radians(angle))
        left_heat_distance = distance - sin_angle
        right_heat_distance = distance + sin_angle
        return left_heat_distance, right_heat_distance

    def get_food_sensor_distances(self, distance, angle):
        sin_angle = math.sin(math.radians(angle))
        left_food_distance = distance - sin_angle
        right_food_distance = distance + sin_angle
        return left_food_distance, right_food_distance
### get sensor distance for heat and food seperately

    def compute_speed(self, left_distance, right_distance, lightness):
        if self.vehicle_type == 'crossed':
            left_speed = (self.speed_parameters[0] / (right_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
            right_speed = (self.speed_parameters[0] / (left_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
        else:
            left_speed = (self.speed_parameters[0] / (left_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
            right_speed = (self.speed_parameters[0] / (right_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
        
        combined_speed = ((left_speed + right_speed) + lightness * 10) / 2
    ### the speed will be quicker when the lightness is positive (brighter), and slower when darker.

        return left_speed, right_speed, combined_speed

    def compute_turn_amount(self, left_speed, right_speed):
        turn_amount = self.turn_parameters[0] * (right_speed - left_speed)
        return turn_amount

    def move(self, lightness):
            combined_heat_speed = 0
            combined_heat_turn_amount = 0

            combined_food_speed = 0
            combined_food_turn_amount = 0

            #count_food = 0

            lost_heat = 0
            lost_food = 0

            for current_input in self.input_heat_list:
                input_heat_distance, input_heat_angle = self.get_heat_input_information(current_input.position())
                left_heat_distance, right_heat_distance = self.get_heat_sensor_distances(input_heat_distance, input_heat_angle)
                
                left_heat_speed, right_heat_speed, average_heat_speed = self.compute_speed(left_heat_distance, right_heat_distance, lightness)
                heat_turn_amount = self.compute_turn_amount(left_heat_speed, right_heat_speed)
                combined_heat_turn_amount += heat_turn_amount
                combined_heat_speed += average_heat_speed


                lost_heat = 30 - self.temperature
            ### the change in temperature of the turtle

                if left_heat_distance >= 0 and left_heat_distance <= 100 and right_heat_distance >= 0 and right_heat_distance <= 100:
                    self.temperature = 30
            ### the temperature will be reset to 30 when turtles reach the range (between 0 and 100) of the heat source

            for current_input in self.input_food_list:
                input_food_distance, input_food_angle = self.get_food_input_information(current_input.position())
                left_food_distance, right_food_distance = self.get_food_sensor_distances(input_food_distance, input_food_angle)
                left_food_speed, right_food_speed, average_food_speed = self.compute_speed(left_food_distance, right_food_distance, 0)
                food_turn_amount = self.compute_turn_amount(left_food_speed, right_food_speed)
                combined_food_turn_amount += food_turn_amount
                combined_food_speed += average_food_speed

                lost_food = self.hunger
            ### the change in hunger of the turtle

                if left_food_distance <= 100 and left_food_distance >= 0 and right_food_distance <= 100 and right_food_distance >= 0:
                    self.hunger = 0
            ### the hunger will be reset to 0 when turtles reach the range (between 0 and 100) of the food source
                if left_food_distance <= 15 and left_food_distance >= 0 and right_food_distance <= 15 and right_food_distance >= 0:
                    current_input.count_food()
            ### call the function to count how many times the food source has been comsumed.



            for current_input in self.input_food_list:
                if current_input.quantity == 0:
                    current_input.hideturtle()
                    self.input_food_list.remove(current_input)
            ### if the food source being consumed by the turtles, the food sources disappear.


            if lost_food >= lost_heat:
                combined_turn_amount = combined_food_turn_amount
                combined_speed = combined_food_speed
            else:
                combined_speed = combined_heat_speed
                combined_turn_amount = combined_heat_turn_amount 
            print("turtle speed:") 
            print(combined_speed)
            ### compare the loss in food and heat of the turtle, go to the source that the turtle lost more.

            try:
                self.right(combined_turn_amount)
            except:
                print(combined_turn_amount)
            
            self.forward(combined_speed)
            self.moves += 1

def create_screen():
    wn = turtle.Screen()
    wn.colormode(255)
    wn.setup(1200, 800)
    wn.title("Vehicle 2")
    wn.tracer(0, 0)
    return wn


def main():
    wn = create_screen()

    wn.register_shape('sun.gif')
    wn.register_shape('food.gif')

    lightness = 50
### brightness of the heat source originally.
    temperature = 30
    hunger = 0
### initial state for each turtle

    num_vehicles = 5
    num_heat_sources = 4
    num_food_sourves = 8

    vehicle_list = []
    input_heat_list = []
    input_food_list = []

    for i in range(num_heat_sources):
        input_heat_list.append(HeatSource(lightness))

    for i in range(num_food_sourves):
        input_food_list.append(FoodSource())

    for i in range(num_vehicles):
        vehicle_list.append(Vehicle2(input_heat_list, input_food_list, i, "crossed", temperature, hunger))

    wn.update()

    while True:
        for j in range(num_heat_sources):
            lightness = input_heat_list[j].lightness_change(lightness)
    ### change the lightness according to sin using lightness_change() function
        for j in range(num_vehicles):
            vehicle_list[j].evaluate_temperature()
            count_food = vehicle_list[j].evaluate_hunger()
            vehicle_list[j].move(lightness)
    ### evaluate each turtles inner state and move according to temperature & hunger
        wn.update()

    if len(input_food_list) == 0:
        wn.bye()
    ### if no food is existing, the world ends.

main()
