# This drawing module assumes the rail is moving toward the positive x direction.
# (i.e. overall only the x coordinate will get incremented)

from typing import Tuple
import random


def _draw_line(x1: int, x2: int, y1: int, y2: int, z1: int, z2: int, block_type: str, **attr) -> str:
    return f'''<DrawLine
        x1="{x1}" y1="{y1}" z1="{z1}"
        x2="{x2}" y2="{y2}" z2="{z2}"
        type="{block_type}" {' '.join(map(lambda kv: f'{kv[0]}="{kv[1]}"', attr.items()))}
    />'''


def _draw_block(x: int, y: int, z: int, block_type: str, **attr) -> str:
    return f'''<DrawBlock
        x="{x}" y="{y}" z="{z}"
        type="{block_type}" {' '.join(map(lambda kv: f'{kv[0]}="{kv[1]}"', attr.items()))}
    />'''


def _draw_cuboid(x1: int, x2: int, y1: int, y2: int, z1: int, z2: int, block_type: str, **attr) -> str:
    return f'''<DrawCuboid
        x1="{x1}" y1="{y1}" z1="{z1}"
        x2="{x2}" y2="{y2}" z2="{z2}"
        type="{block_type}" {' '.join(map(lambda kv: f'{kv[0]}="{kv[1]}"', attr.items()))}
    />'''


def _draw_red_stone_and_golden_rail_as_line(x1: int, x2: int, y1: int, y2: int, z1: int, z2: int) -> str:
    """Please notice that the position y is based on golden_rail"""
    return f'{_draw_line(x1, x2, y1 - 1, y2 - 1, z1, z2, "redstone_block")}\n' \
        f'{_draw_line(x1, x2, y1, y2, z1, z2, "golden_rail")}'


def _generate_beats(x1: int, x2: int, y: int, z: int, prob: float):
    ret = ''

    for x in range(x1, x2, + 1):
        if random.random() > prob:
            ret += _draw_block(x, y + 1, z - 1, 'air')
        if random.random() > prob:
            ret += _draw_block(x, y + 1, z + 1, 'air')
    
    return ret


def draw_branch_left(entry_x: int, entry_y: int, entry_z: int) -> Tuple[str, Tuple[int, int, int]]:
    """Draw T shape branch with correct path on the left side
    
    :param entry_x: entry point x position
    :param entry_y: entry point y position
    :param entry_z: entry point z position
    :returns XML for the branch and entry point for next map component
    """
    return f'''<!--Clear-->
    {_draw_cuboid(entry_x + 11, entry_x, entry_y, entry_y - 4, entry_z - 4, entry_z + 6, "air")}
    
    <!--Lava pool for punish :(-->
    {_draw_cuboid(entry_x + 4, entry_x, entry_y - 1, entry_y - 3, entry_z + 3, entry_z + 6, "iron_block")}
    {_draw_cuboid(entry_x + 3, entry_x, entry_y - 1, entry_y - 1, entry_z + 4, entry_z + 5, "lava")}
    {_draw_cuboid(entry_x - 1, entry_x - 1, entry_y - 1, entry_y - 16, entry_z + 4, entry_z + 5, "lava")}

    <!--Redstone Block and Golden Rail-->
    {_draw_red_stone_and_golden_rail_as_line(entry_x, entry_x + 6, entry_y, entry_y, entry_z, entry_z)}
    {_draw_red_stone_and_golden_rail_as_line(entry_x + 7, entry_x + 7, entry_y, entry_y, entry_z + 1, entry_z + 4)}

    {_draw_block(entry_x + 7, entry_y - 1, entry_z + 5, "iron_block")}
    {_draw_block(entry_x + 7, entry_y, entry_z + 5, "rail")}
    {_draw_red_stone_and_golden_rail_as_line(entry_x + 5, entry_x + 6, entry_y, entry_y, entry_z + 5, entry_z + 5)}
    {_draw_block(entry_x + 4, entry_y, entry_z + 5, "golden_rail")}

    {_draw_block(entry_x + 7, entry_y - 1, entry_z, "iron_block")}
    {_draw_block(entry_x + 7, entry_y, entry_z, "rail")}

    {_draw_red_stone_and_golden_rail_as_line(entry_x + 7, entry_x + 7, entry_y, entry_y, entry_z - 1, entry_z - 3)}
    {_draw_block(entry_x + 7, entry_y - 1, entry_z - 4, "iron_block")}
    {_draw_block(entry_x + 7, entry_y, entry_z - 4, "rail")}
    {_draw_red_stone_and_golden_rail_as_line(entry_x + 8, entry_x + 9, entry_y, entry_y, entry_z - 4, entry_z - 4)}
    {_draw_block(entry_x + 10, entry_y - 1, entry_z - 4, "iron_block")}
    {_draw_block(entry_x + 10, entry_y, entry_z - 4, "rail")}
    {_draw_red_stone_and_golden_rail_as_line(entry_x + 10, entry_x + 10, entry_y, entry_y, entry_z - 3, entry_z - 1)}
    {_draw_block(entry_x + 10, entry_y - 1, entry_z, "iron_block")}
    {_draw_block(entry_x + 10, entry_y, entry_z, "rail")}
    {_draw_red_stone_and_golden_rail_as_line(entry_x + 11, entry_x + 19, entry_y, entry_y, entry_z, entry_z)}

    <!--Redstone Circuit-->

    {_draw_line(entry_x + 5, entry_x + 7, entry_y - 2, entry_y - 4, entry_z + 3, entry_z + 3, "iron_block")}
    {_draw_line(entry_x + 4, entry_x + 7, entry_y, entry_y - 3, entry_z + 3, entry_z + 3, "air")}
    {_draw_line(entry_x + 4, entry_x + 7, entry_y, entry_y - 3, entry_z + 3, entry_z + 3, "redstone_wire")}

    {_draw_block(entry_x + 4, entry_y, entry_z + 4, "air")}
    {_draw_block(entry_x + 4, entry_y, entry_z + 4, "redstone_wire")}

    {_draw_block(entry_x + 3, entry_y, entry_z + 4, "iron_block")}
    {_draw_block(entry_x + 3, entry_y + 1, entry_z + 4, "air")}
    {_draw_block(entry_x + 3, entry_y + 1, entry_z + 4, "redstone_wire")}

    {_draw_line(entry_x + 4, entry_x + 2, entry_y + 1, entry_y + 1, entry_z + 3, entry_z + 3, "iron_block")}
    {_draw_line(entry_x + 4, entry_x + 2, entry_y + 2, entry_y + 2, entry_z + 3, entry_z + 3, "air")}
    {_draw_line(entry_x + 4, entry_x + 2, entry_y + 2, entry_y + 2, entry_z + 3, entry_z + 3, "redstone_torch")}
    {_draw_block(entry_x + 3, entry_y + 2, entry_z + 3, "redstone_wire")}

    {_draw_line(entry_x + 4, entry_x + 2, entry_y, entry_y, entry_z + 2, entry_z + 2, "iron_block")}
    {_draw_line(entry_x + 4, entry_x + 2, entry_y + 1, entry_y + 1, entry_z + 2, entry_z + 2, "air")}
    {_draw_line(entry_x + 4, entry_x + 2, entry_y + 1, entry_y + 1, entry_z + 2, entry_z + 2, "redstone_wire")}
    {_draw_block(entry_x + 3, entry_y, entry_z + 2, "air")}
    {_draw_block(entry_x + 3, entry_y + 1, entry_z + 2, "air")}

    {_draw_line(entry_x + 4, entry_x + 2, entry_y + 1, entry_y + 1, entry_z + 1, entry_z + 1, "redstone_block")}
    {_draw_block(entry_x + 3, entry_y  + 1, entry_z + 1, "air")}

    {_draw_block(entry_x + 8, entry_y - 4, entry_z + 3, "iron_block")}
    {_draw_block(entry_x + 8, entry_y - 3, entry_z + 3, "air")}
    {_draw_block(entry_x + 8, entry_y - 3, entry_z + 3, "redstone_wire")}

    {_draw_line(entry_x + 9, entry_x + 9, entry_y - 2, entry_y - 4, entry_z, entry_z + 3, "iron_block")}
    {_draw_line(entry_x + 9, entry_x + 9, entry_y - 1, entry_y - 3, entry_z, entry_z + 3, "air")}
    {_draw_line(entry_x + 9, entry_x + 9, entry_y - 1, entry_y - 3, entry_z, entry_z + 3, "redstone_wire")}

    {_draw_block(entry_x + 8, entry_y - 1, entry_z, "iron_block")}
    {_draw_block(entry_x + 8, entry_y, entry_z, "air")}
    {_draw_block(entry_x + 8, entry_y, entry_z, "redstone_wire")}
    ''', (entry_x + 20, entry_y, entry_z)


def draw_rail_line_with_beats(entry_x: int, entry_y: int, entry_z: int, length: int) -> Tuple[str, Tuple[int, int, int]]:
    return f'''<!--Clear-->
    {_draw_line(entry_x, entry_x + length, entry_y, entry_y, entry_z, entry_z, "air")}
    {_draw_line(entry_x, entry_x + length, entry_y - 1, entry_y - 1, entry_z, entry_z, "air")}
    {_draw_line(entry_x, entry_x + length, entry_y + 1, entry_y + 1, entry_z - 1, entry_z - 1, "air")}
    {_draw_line(entry_x, entry_x + length, entry_y + 1, entry_y + 1, entry_z + 1, entry_z + 1, "air")}
    
    <!--Drawing-->
    {_draw_red_stone_and_golden_rail_as_line(entry_x, entry_x + length, entry_y, entry_y, entry_z, entry_z)}
    {_draw_line(entry_x, entry_x + length, entry_y + 1, entry_y + 1, entry_z - 1, entry_z - 1, "wool", colour="YELLOW")}
    {_draw_line(entry_x, entry_x + length, entry_y + 1, entry_y + 1, entry_z + 1, entry_z + 1, "wool", colour="LIGHT_BLUE")}
    {_generate_beats(entry_x, entry_x + length, entry_y, entry_z, 1)}
    ''', (entry_x + length + 1, entry_y, entry_z)


def draw_starting_point(entry_x: int, entry_y: int, entry_z: int) -> Tuple[str, Tuple[int, int, int]]:
    return f'''<!--Clear Beacon Area-->
    {_draw_cuboid(entry_x + 1, entry_x - 1, entry_y - 1, entry_y + 2, entry_z - 1, entry_z + 1, "air")}

    <!--Beacon-->
    {_draw_cuboid(entry_x + 1, entry_x - 1, entry_y - 1, entry_y, entry_z - 1, entry_z + 1, "gold_block")}
    {_draw_block(entry_x, entry_y + 1, entry_z, "beacon")}
    {_draw_block(entry_x, entry_y + 2, entry_z, "stained_glass", colour="YELLOW")}

    <!--Rail-->
    {_draw_cuboid(entry_x + 2, entry_x + 7, entry_y, entry_y - 1, entry_z, entry_z, "air")}
    {_draw_line(entry_x + 2, entry_x + 7, entry_y - 1, entry_y - 1, entry_z, entry_z, "iron_block")}
    {_draw_line(entry_x + 2, entry_x + 6, entry_y, entry_y, entry_z, entry_z, "golden_rail")}
    {_draw_block(entry_x + 7, entry_y, entry_z, "rail")}

    <!--Cart-->
    <DrawEntity x="{entry_x + 2.5}" y="{entry_y + 0.1}" z="{entry_z + 0.5}" type="MinecartRideable"/>

    <!--Start-->
    {_draw_block(entry_x + 2, entry_y - 1, entry_z + 1, "iron_block")}
    {_draw_block(entry_x + 2, entry_y, entry_z + 1, "redstone_wire")}

    {_draw_block(entry_x + 2, entry_y, entry_z + 3, "iron_block")}
    {_draw_block(entry_x + 2, entry_y + 1, entry_z + 3, "redstone_wire")}
    
    {_draw_block(entry_x + 3, entry_y, entry_z + 3, "iron_block")}
    {_draw_block(entry_x + 3, entry_y + 1, entry_z + 3, "redstone_wire")}
    
    {_draw_block(entry_x + 3, entry_y, entry_z + 2, "iron_block")}
    {_draw_block(entry_x + 3, entry_y + 1, entry_z + 2, "redstone_wire")}

    {_draw_block(entry_x + 3, entry_y + 1, entry_z + 1, "redstone_block")}

    {_draw_block(entry_x + 2, entry_y, entry_z + 2, "unlit_redstone_torch", face="NORTH")}
    ''', (entry_x + 8, entry_y, entry_z)


def draw_finish_line(entry_x: int, entry_y: int, entry_z: int) -> Tuple[str, Tuple[int, int, int]]:
    return f'''
    {_draw_cuboid(entry_x + 10, entry_x, entry_y - 1, entry_y - 10, entry_z - 6, entry_z + 6, "stained_glass", colour="PINK")}
    {_draw_cuboid(entry_x + 9, entry_x + 1, entry_y - 1, entry_y - 8, entry_z -5, entry_z + 5, "water")}
    {_draw_block(entry_x, entry_y - 1, entry_z, "iron_block")}
    {_draw_block(entry_x, entry_y, entry_z, "golden_rail")}
    ''', (entry_x + 11, entry_y, entry_z)


map_generated = _draw_cuboid(-256, 256, -256, 256, -256, 256, "air")
xml, next_start = draw_starting_point(0, 10, 0)

# map_generated += xml
# xml, next_start = draw_branch_left(*next_start)

# map_generated += xml
# xml, next_start = draw_branch_left(*next_start)

# map_generated += xml
# xml, next_start = draw_rail_line_with_beats(*next_start, 20)

# map_generated += xml
# xml, next_start = draw_branch_left(*next_start)

map_generated += xml
xml, next_start = draw_rail_line_with_beats(*next_start, 500)

map_generated += xml
xml, _ = draw_finish_line(*next_start)
map_generated += xml
