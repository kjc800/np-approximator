# NP-Approximation Algorithm

## Problem and Goal

Project solves the given problem:

### Problem Statement
You are given an undirected graph G = (L,E) where each vertex in L is a location. You are also given a starting location s, and a list H of unique locations that correspond to homes. The weight of each edge (u,v) is the length of the road between locations u and v, and each home in H denotes a location that is inhabited by a student. Driving the bus down a road takes energy, and the amount of energy expended is proportional to the length of the road. For every unit of distance traveled, the driver of the bus expends 2/3 units of energy, and a walking student expends 1 unit of energy. The car must start and end at s, and every student must return to their home in H.
You must return a list of vertices v that is the tour taken by the bus (cycle with repetitions allowed), as well as a list of drop-off locations at which the students get off. You may only drop students off at vertices visited by the bus, and multiple students can be dropped off at the same location.

### Goal
Produce a route and sequence of drop-offs that minimizes total energy expenditure, which is the sum of the driver's energy spent driving and the total energy that all of the students spend walking. Note students do not expend any energy while sitting in the bus. It is assumed that the students will take the shortest path home from whichever location they are dropped off at.

## Design

### Naive Baselines:
#### Traveling Salesman Problem Solver: 
Main Idea: Use a TSP solver from the D-Wave Network X Library to find a tour visiting all the homes. Since the TSP solver uses a complete graph, add a dummy edge with infinite weight between all unconnected vertices. 

Reasoning: Metric TSP problem reduces to the drive student’s home problem when the driver takes 1/2 the energy of a student walking.

### Non-Naive Tour Finding:
#### Repeated Dijkstra’s:
Main Idea: Create a set H containing all the home vertices. Run Dijkstra’s shortest path algorithm from the starting location to each home in the set. Select the shortest path found and add that path to the tour. Remove the home pertaining to that shortest path from the set H. Repeatedly run Dijkstra’s on the last home removed and set H and continue to add the shortest path to the tour. When the set H is empty, run Dijkstra’s shortest path from the last home to the starting point. The finished tour should be the shortest tour that goes through every home.

Reasoning: This algorithm will guarantee to touch every home location. This tour would provide the optimal solution if we always drop a student at a home. 

#### Iterative Improvement Algorithm:
Main Idea: Create a random tour visiting all home locations (or use the Repeated Dijkstra’s tour from above). Use iterative improvement (similar to a Min-Conflicts/Local Search Algorithm) to gradually reduce the cost of the tour until no other optimization can be made. We would choose a home and compare the cost of visiting the home to the cost of dropping the student off at a location nearby. If the overall cost is less, set the drop off location to that location and repeat the process. Then move on to the next home. Repeat until all homes have gone through this process.

Reasoning: This algorithm is guaranteed to touch every home location and attempts to find optimal drop-off locations. We could also run the Repeated Dijkstra’s algorithm above and use iterative improvement on that tour as well. 

#### Random Improvement Algorithm:
Main Idea: Create a tour using the Repeated Dijkstra’s algorithm. The current drop off locations will be the location of each home and the cost of this tour will be an upper bound. Improve the tour by considering the neighboring vertices of the drop-off locations along with the current drop-off locations. The new drop-off locations will be determined randomly based on a probability distribution that is proportional to the degree of the vertex. Higher degree will equate to a higher probability. Repeat for total number of neighboring drop-off locations.

Reasoning: The algorithm aims to find optimal drop-off locations quickly by seeking common vertices. If more than one student will be dropped at a location and at least one will have to walk, then vertices that have larger degrees will have a higher chance of connecting the drop-off location to the respective student home.

## Implementation
### Random Improvement Algorithm: (score = 55):
The algorithm would create a tour using the Repeated Dijkstra’s algorithm and then improve the cycle. The current cycle would begin with the drop off locations being all of the homes and the cost of this cycle would act as a baseline cost. Two random drop off locations, which we called ‘stars’, would be selected to be changed, which would create a different cycle. We would move these ‘stars’ based on a probability distribution that is proportional to the degrees of the neighboring vertices. A higher degree would equate to a higher probability. After moving, we would check the cost of the new cycle and compare it with the current best cost (which initially is the cost of the baseline cycle). If the new cycle had a better cost, we would continue with the algorithm and move another two random ‘stars’ from the new cycle. If the cycle did not have a better cost, we would continue the algorithm on this bad cycle for thirty iterations to see if it would possibly improve. The entire program ran for five minutes until ending and creating the outputs.

### Iterative Improvement Algorithm (Unsuccessful):
We tried implementing a different version of the random improvement algorithm where, after finding a tour through all homes, we would go through each home and attempt to find a more optimal dropoff location by comparing the overall tour cost. This method ended up outputting costs that were larger than the Random Improvement Algorithm, so we decided to not pursue the idea.

### Repeated Dijkstra’s (score = 40):
The algorithm would take in the graph, a start index, and a list of homes and return a tour visiting all homes and returning back to the start index. We would start at the start index and, from there, find the closest home from the start using Dijkstra’s methods from NetworkX. We would add that path to our cycle. We would then find the path to the next closest home from our current home, adding that path to our cycle. We would repeat this until we had visited all homes. In the end, we would find the path from the last visited home to our start index to complete the tour. We ran this method on all the inputs and we saw a quality of around 40 for all inputs. 

### Repeated Dijkstra’s + Random Improvement Algorithm: (score = 37):
We then fixed the bug in our previous implementation of the Random Improvement Algorithm by using the Repeated Dijkstra’s algorithm above to find cycles before randomly moving drop off locations. This improvement got us down to a quality of 37 across all inputs.

## Issues

A majority of the issues we faced during this project were all during the creation of our Repeated Dijkstra’s implementation. 
One problem we ran into was not correctly getting the closest home to move to. The algorithm was expected to find the closest home from the start, add that path to the cycle, and then find the next closest home starting from the previous home found. Instead, we were simply iterating through the list of homes in the order given and creating the cycle from that order of homes. This resulted in a longer cycle than necessary, which ultimately gave us a larger output value.
Another issue we ran into was when there were overlapping homes. When creating the cycle, there would be an off-by-one error and the home would be skipped in the cycle. After hours of debugging, we decided to reimplement the entire algorithm, which ultimately fixed the issue and produced a correct cycle that included all the homes.
