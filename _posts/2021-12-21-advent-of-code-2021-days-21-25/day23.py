from functools import cache

with open('day23-input.txt') as file:
    day23 = file.read()

print(day23)
# Extract the letters into a list
letters = [c for c in day23 if c.isalpha()]
letters = letters[:4], letters[4:]

# Use tuples instead of lists, because they are fixed in size, just like the
#  rooms/hallway
rooms = [(letter1, letter2) for letter1, letter2 in zip(*letters)]
# The hallway is 11 empty spaces, represented by None
hallway = (None, ) * 11
# The initial state is represented with a tuple of tuples
initial_state = (hallway, *rooms)

target_state = ((None, ) * 11, ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'))
target_rooms = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
room_to_hall = {1: 2, 2: 4, 3: 6, 4: 8}
hall_to_room = {2: 1, 4: 2, 6: 3, 8: 4}
energy_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def get_possible_moves(state):
  # For each room, consider moving the top-most amphipods
  for i in range(1, 5):
    # Look for the first non-empty space
    if state[i][0] is not None:
      # The top spot is occupied
      top_loc = 0
    elif state[i][1] is not None:
      # The bottom spot is occupied 
      top_loc = 1
    else:
      # Otherwise, nothing in this room so continue
      continue
    
    # In order to mutate the state, need to convert to list of lists
    state_list = list(map(list, state))
    letter = state_list[i][top_loc]
    
    # If this letter is in the right room, and everything below it is as well
    if target_rooms[letter] == i and \
        all(letter == letter_below for letter_below in state[i][top_loc:]):
      continue # Don't move it
          
    steps = top_loc
    # Move it
    state_list[i][top_loc] = None
    possible_locs = []
    
    # Find spaces in the hallway
    # Look to the left of the room first
    for j in range(room_to_hall[i]):
      # If not in front of the door
      if j not in [2, 4, 6, 8]:
        possible_locs.append(j)
      # If that space in the hallway is occupied, it is not possible to move
      if state_list[0][j] is not None:
        possible_locs.clear()
    for j in range(room_to_hall[i], 11):
      if state_list[0][j] is not None:
        break
      if j not in [2, 4, 6, 8]:
        possible_locs.append(j)
    
    # The new states will have unique hallways, as a letter moves from a room
    new_state = list(map(tuple, state_list))
    hallway = state[0]
    
    for loc in possible_locs:
      hallway_list = list(hallway)
      hallway_list[loc] = letter
      new_state[0] = tuple(hallway_list)
      # Count the number of steps to get to this space, and multiply by energy
      energy = (steps + 1 + abs(loc - room_to_hall[i])) * energy_costs[letter]
      yield tuple(new_state), energy
      
  # For each amphipod in the hallway, consider moving into rooms
  for i,letter in enumerate(state[0]):
    if letter is None: continue
    
    # Find the target room for this letter
    target_room = target_rooms[letter]
    # And its current occupants
    room_letters = set(state[target_room]).discard(None)
    # And the hallway location right outside
    target_hallway = room_to_hall[target_room]
    # If the room has other letters in it, don't both moving into it
    if room_letters and {letter} != room_letters:
      continue
    
    # If to the left of the target location
    if i < target_hallway:
      # Consider all locations to the left
      hall_locs = slice(i + 1, target_hallway + 1)
    else:
      # Otherwise, all locations to the right
      hall_locs = slice(target_hallway, i)
    
    # If there is an amphipod in the way, break
    for loc in state[0][hall_locs]:
      if loc is not None:
        break
    else:
      steps = abs(i - target_hallway)
      state_list = list(map(list, state))
      # Remove it from the hall
      state_list[0][i] = None
      # Get the list of current room occupants
      room_list = state_list[target_room]
      
      # Consider all locations in the room
      for room_loc, other_letter in reversed(list(enumerate(room_list))):
        if other_letter is None: break
      
      # If the top location is empty (as expected) move the amphipod there
      if room_list[room_loc] is None:
        print('found error\n\n')
        print(letter)
        print(state_list)
        print(room_list)
        print(room_loc)
        print('found error\n\n')
        assert room_list[room_loc] is None

      room_list[room_loc] = letter
      steps += room_loc + 1
      
      energy = steps * energy_costs[letter]
      yield tuple(map(tuple, state_list)), steps * energy
      
@cache
def steps_to_target(state):
  if state == target_state:
      print('target')
      return 0
  
  #print(state)
  possible_costs = []
  
  for new_state, energy in get_possible_moves(state):
    possible_costs.append(energy + steps_to_target(new_state))
    
  return min(possible_costs)


import sys
sys.setrecursionlimit(30000)

#part1 = steps_to_target(initial_state)
#print(part1)

for new_state, energy in get_possible_moves(initial_state):
    print(new_state)
    print(energy)

    print('new states\n')
    for newer_state, energy in get_possible_moves(new_state):
        print(newer_state)
        print(energy)