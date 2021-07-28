import heapq
import collections

#a class to store runway objects
class Runway:
    def __init__(self, size):
        self.size = size


#a class to store aircraft object
class Aircraft:
    def __init__(self, index, weight, passengers):
        self.index = index
        self.weight = weight
        self.passengers = passengers


#a class for a priority queue that uses min heap for sorting aircrafts based on number of passengers
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
    def push(self, item, priority):
        self._index += 1
        heapq.heappush(self._queue, (-priority, self._index, item))
    def pop(self):
        self._index -= 1
        return heapq.heappop(self._queue)[-1]
    def __len__(self):
        return self._index


count = 0
runways_info= []
aircrafts_list = []

#use a reader object to consume input file info
with open('input_data_aircraft_queue.txt', 'r') as f:
    for line in f:
        if count != 0:
            aircrafts_list.append(line)
        else:
            runways_info.append(line)
            count += 1


#store input file info about runways
runways = runways_info[0].split()
runways_dict = collections.defaultdict(Runway)
count = 1
for i in range(len(runways)):
    if runways[i] == 'small':
        for _ in range(int(runways[i-1])):
            runways_dict[count] = Runway('small')
            count += 1
    elif runways[i] == 'medium':
        for _ in range(int(runways[i-1])):
            runways_dict[count] = Runway('medium')
            count += 1
    elif runways[i] == 'large':
        for _ in range(int(runways[i-1])):
            runways_dict[count] = Runway('large')
            count += 1


#store intput file info about aircrafts
count = 1
aircraft_dict = collections.defaultdict(Aircraft)
for aircraft in aircrafts_list:
    aircraft = aircraft.split()
    aircraft_dict[count] = Aircraft(count, aircraft[1].replace(',',''), aircraft[3])
    count += 1


#create 3 separate queues of aircrafts for each runway based on weight
large_aircraft_pq = PriorityQueue()
medium_aircraft_pq = PriorityQueue()
small_aircraft_pq = PriorityQueue()


#sort aircrafts in each queue based on the number of passengers
for aircraft in aircraft_dict.values():
    if int(aircraft.weight) < 200000:
        small_aircraft_pq.push(aircraft, int(aircraft.passengers))
    elif int(aircraft.weight) < 500000:
        medium_aircraft_pq.push(aircraft, int(aircraft.passengers))
    else:
        large_aircraft_pq.push(aircraft, int(aircraft.passengers))


#a class whose purpose is to produce a dictionary with keys representing runways and values representing aircrafts landing on respectives runways optimally
class Airport:
    def __init__(self):
        self.no_small_aircrafts = False
        self.no_medium_aircrafts = False
        self.no_large_aircrafts = False
        self.output_runway_dict = collections.defaultdict(list)

    def populate_output(self):
        for key in runways_dict.keys():
            if runways_dict[key].size == 'small' and not self.no_small_aircrafts:
                self.output_runway_dict[tuple((key, 'small'))].append(small_aircraft_pq.pop())
                if not small_aircraft_pq: 
                    self.no_small_aircrafts = True

            #if no small-size aircrafts remain in the queue, skip the runway that only fits small-size aircrafts
            elif runways_dict[key].size == 'small' and self.no_small_aircrafts:
                pass
                
            elif runways_dict[key].size == 'medium' and not self.no_medium_aircrafts:
                self.output_runway_dict[tuple((key, 'medium'))].append(medium_aircraft_pq.pop())
                if not medium_aircraft_pq: self.no_medium_aircrafts = True

            #if no mid-size aircrafts remain in the queue, allow small-size aircrafts land in the runway normally for mid-size aircrafts
            elif runways_dict[key].size == 'medium' and self.no_medium_aircrafts:
                self.output_runway_dict[tuple((key, 'medium'))].append(small_aircraft_pq.pop())

            elif runways_dict[key].size == 'large' and not self.no_large_aircrafts:
                self.output_runway_dict[tuple((key, 'large'))].append(large_aircraft_pq.pop())
                if not large_aircraft_pq: self.no_large_aircrafts = True

            #if no large-size aircrafts remain in the queue, allow small- and mid-size aircrafts land in the runway normally for large-size aircrafts
            elif runways_dict[key].size == 'large' and self.no_large_aircrafts:
                if not medium_aircraft_pq:
                    self.output_runway_dict[tuple((key, 'large'))].append(medium_aircraft_pq.pop())
                elif not small_aircraft_pq:
                    self.output_runway_dict[tuple((key, 'large'))].append(small_aircraft_pq.pop())

airport = Airport()

#continue while loop untill no aircraft objects remains in any priority queue
while small_aircraft_pq or medium_aircraft_pq or large_aircraft_pq:
    airport.populate_output()

#print out answer in requested format
for key, values in airport.output_runway_dict.items():
    output = []
    for value in values:
        output += ['Aircraft ', str(value.index), ' (', str(value.weight), ' pounds, ', str(value.passengers), ' passengers), ']
    output = ''.join(output)

    print('Runway {0} ({1}): {2}'.format(key[0], key[1], output))


#FOLLOW-UP QUESTIONS:

# 1) How would we add support for carrier-specific runways?  For example, one runway can only allow Delta aircraft

#Aircraft and Runway class would each have an additional variable representing a carrier. Then when we pop an aircraft from any priority queue,
#we would add it only to the matching runway, which is a key in self.output_runway_dict, which is a variable in Airport class.


# 2) If we were dealing with thousands of planes, how could we make this algorithm more efficient?

#We could assume that larger planes transport more people, so we could prioritize larger planes in an algorithm, while it currently depends on the wording of input file.
#We could check the total number of aircrafts and/or passengers remaining in each priority queue to continue popping elements from a queue with larger total population,
#especially useful when reassigning those aircrafts to a recently-emptied runways.  

# 3) If we added a new priority called "departure time" and weighted the order based on departure time and number of passengers, how would we implement this?

# Priority Queue class would have a method that generates a value for priority (see line 25 above), which is a weighted combination of time and number of passengers. 
