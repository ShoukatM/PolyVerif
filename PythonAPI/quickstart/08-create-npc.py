#!/usr/bin/env python3
#
# Copyright (c) 2019-2020 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

from environs import Env
import lgsvl

env = Env()

sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1"), env.int("LGSVL__SIMULATOR_PORT", 8181))
if sim.current_scene == "BorregasAve":
    sim.reset()
else:
    sim.load("BorregasAve")

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]
sim.add_agent(env.str("LGSVL__VEHICLE_0", "JaguarRosCustomSensor"), lgsvl.AgentType.EGO, state)

forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])

# Spawns one of each of the listed types of NPCS
# The first will be created in front of the EGO and then they will be created to the left
# The available types of NPCs can be found in NPCManager prefab
for i, name in enumerate(["Sedan", "SUV", "Jeep", "Hatchback"]):
    state = lgsvl.AgentState()

    # Spawn NPC vehicles 10 meters ahead of the EGO
    state.transform.position = spawns[0].position + (10 * forward) - (4.0 * i * right)
    state.transform.rotation = spawns[0].rotation
    sim.add_agent(name, lgsvl.AgentType.NPC, state)
	
sim.run();