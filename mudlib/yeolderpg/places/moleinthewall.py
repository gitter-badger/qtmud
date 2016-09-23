import qtmud
from mudlib.yeolderpg.qualities import room

bar = room.apply(qtmud.new_thing())
kitchen = room.apply(qtmud.new_thing())

bar.exits = {'kitchen': kitchen}
kitchen.exits = {'bar': bar}

bar.name = 'Mole in the Wall'
bar.description = 'This is a simple tavern.'
bar.noises = {'listen': ['some sounds']}

kitchen.name = 'Kitchen'
kitchen.description = 'This is a kitchen yup.'