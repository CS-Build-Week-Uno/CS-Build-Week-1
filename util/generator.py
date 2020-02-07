from adventure.models import Room, Player
import random
Room.objects.all().delete()

class Map:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = 0
        y = -1  # (this will become 0 on the first step)
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west

        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and y < size_y - 1:
                room_direction = "n"
                y += 1
            elif direction < 0 and y > 0:
                room_direction = "s"
                y -= 1
            else:
                # If we hit a wall, turn east and reverse direction
                room_direction = "e"
                x += 1
                direction *= -1

            # Create a room in the given direction

            roomName=["No Death", "Not Allowed to die here", "Its ok to die here", "Death of Death", "9 Lives", "1 Life", "A lot of Death", "Life?(Nope just Death)", "Death's Door", "To Die or Not to Die", "Nuke Town"]

            roomDescription=["There shall never be a death in this room", "Physically not allowed to die here, if the rule is broken, the punishment is death", "It's completely ok to die here :)", "Death", "A cat lives in this room, but still has all of its lives", "A scraggly cat lives here, he's on his last life", "“Literally everything is dead", "There is a green plant in front of you that looks alive and healthy, but it's really just plastic and super dead", "There is a door on the roof with satan", "You are given a choice, to read a MLP fanfiction, or die", "You take a 360 no scope to the head, but it's just a hit marker and the enemy is raging out of his mind"]

            randomRoomName = random.choice(roomName)
            randomRoomDescription = random.choice(roomDescription)

            room = Room(room_count, randomRoomName,
                        randomRoomDescription, x, y)
            # room = Room(room_count, "A Generic Room",
            #             "This is a generic room.", x, y)
            # Note that in Django, you'll need to save the room after you create it
            room.save()

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connectRooms(room, room_direction)

            # Update iteration variables
            previous_room = room
            room_count += 1

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)
