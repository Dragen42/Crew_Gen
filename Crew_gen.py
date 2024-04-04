import random
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import KoboldApiLLM
import os
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate



# A list of array of objects containing the crew members with their details, personality traits, and alliances


crew_members = {
    "Aisha": {"name": "Dr. Aisha Patel",
              "age": "38",
              "profession": "Chief Scientist",
              "personality": "Ambitious and pragmatic, with a knack for leveraging scientific discoveries for personal gain",
              "alliance": "CPC",
              "description": "Short hair with augmented reality glasses, practical attire with tech gadgets. CPC-branded patch."},
    "Lena": {"name": "Maj. Lena Svensson",
             "age": "40",
             "profession": "Security Chief",
             "personality": "Loyal and strategic, yet harbors a deep-seated mistrust of non-corporate entities",
             "alliance": "Independent Consultant",
             "description": "Cybernetic arm, scar across left cheek, armored clothing. Military and mercenary edge."},
    "Hiroshi": {"name": "Dr. Hiroshi Tanaka",
                "age": "42",
                "profession": "Geologist",
                "personality": "Curious yet secretive, often withholding findings that could alter power dynamics",
                "alliance": "Husqvarna",
                "description": "Worn clothes, old-fashioned yet tech-equipped glasses, carries a rugged multi-use tablet."},
    "Emily": {"name": "Dr. Emily Roche",
              "age": "34",
              "profession": "Astrobiologist",
              "personality": "Idealistic but easily manipulated, her naivety is a cover for gathering intelligence",
              "alliance": "Microsoft",
              "description": "Practical workwear with a cyberpunk flair, vibrant hair streak, Microsoft-branded smartwatch."},
    "Samuel": {"name": "Prof. Samuel Ndlovu",
               "age": "47",
               "profession": "Theoretical Physicist",
               "personality": "Charismatic leader with radical views on technology's role in society",
               "alliance": "Academic",
               "description": "Smart rugged attire, jacket with integrated interface. Forward-thinking academic."},
    "Nina": {"name": "Nina Petrova",
             "age": "29",
             "profession": "Robotics Engineer",
             "personality": "Innovative and rebellious, often at odds with corporate bureaucracy",
             "alliance": "Husqvarna",
             "description": "Engineering outfit with HUD visor and multi-tool, patches from tech expos."},
    "Carlos": {"name": "Carlos Rivera",
               "age": "39",
               "profession": "Systems Architect",
               "personality": "Analytical and detached, prioritizes data over human relations",
               "alliance": "Microsoft",
               "description": "Sleek minimalist attire with smart fabrics, mobile computing eyewear, functional clothing with hidden compartments."},
    "Ling": {"name": "Ling Wei",
             "age": "42",
             "profession": "Environmental Engineer",
             "personality": "Eco-centric with a ruthless streak for opponents of environmental projects",
             "alliance": "Husqvarna",
             "description": "Eco-themed clothing with advanced environmental monitoring tech, botanical-inspired tattoo."},
    "Sarah": {"name": "Sarah Al-Hakim",
              "age": "36",
              "profession": "Resource Operations Manager",
              "personality": "Resourceful and persuasive, known for negotiating underhanded deals",
              "alliance": "Independent Contractor",
              "description": "Sharp, commanding look with high-tech accessories, encrypted comms bracelet."},
    "Jackson": {"name": "Jackson Miles",
                "age": "33",
                "profession": "Supply Chain Coordinator",
                "personality": "Charming but deceptive, uses his charisma to mask true intentions",
                "alliance": "Husqvarna",
                "description": "Laid-back rugged look, custom-built logistics interface on jacket sleeve."},
    "Sgt": {"name": "Sgt. Dmitri Volkov",
            "age": "37",
            "profession": "Tactical Officer",
            "personality": "Stoic and disciplined, but his loyalty is bought and sold to the highest bidder",
            "alliance": "Independent Consultant",
            "description": "Tactical vest, cybernetic eye enhancement, military posture."},
    "Li": {"name": "Li Mei",
           "age": "32",
           "profession": "Cybersecurity Specialist",
           "personality": "Genius-level intellect with a penchant for cyber-espionage and a disdain for ethics",
           "alliance": "Microsoft",
           "description": "Lightweight, dark clothing for stealth, cybernetic enhancements for hacking."},
    "Sofia": {"name": "Dr. Sofia Gonzalez",
              "age": "41",
              "profession": "Chief Medical Officer",
              "personality": "Compassionate and ethical, yet harbors a dark past that influences medical decisions",
              "alliance": "Doctors Without Borders, MSF",
              "description": "Professional scrubs, compact advanced medical kit."},
    "Jamal": {"name": "Jamal Anwar",
              "age": "28",
              "profession": "Chef",
              "personality": "Lively and empathic, but his conflict-avoidant personality sometimes gets him in trouble",
              "alliance": "The Free Clans of The Solar System",
              "description": "Chef attire with fireproof apron, temperature sensor sleeves, utility belt with culinary tools."}
}

# A mermaid diagram of the Heaven's Sphere Spacecraft. Part of the prompt

HTHS = """
    Map Of The Heavenly Sphere Nuclear Pulse Spacecraft

    A[Harmony of the Spheres Spine] --> B[Vertebrae One: Command and Control Module]
    A --> C[Ring One: Living Quarters and Community Spaces]
    A --> D[Ring Two: Science and Research Labs]
    A --> E[Ring Three: Resource Management and Life Support Systems]
    A --> F[Vertebrae Three: Propulsion and Engineering]
    A --> G[Vertebrae Two: Exploration and Defense]

    B --> B1[Bridge]
    B --> B2[Navigation and Communications Hub]
    B --> B3[Communication Array Control]

    C --> C1[Individual Crew Quarters]
    C --> C2[Communal Dining Area]
    C --> C3[Recreational Facilities]
    C --> C4[Medical Bay]

    C1 --> C1a[Commander Chen Liang's Private Quarters 45, Mission Commander]
    C1 --> C1b[Dr. Aisha Patel's Private Quarters 38, Chief Scientist]
    C1 --> C1c[Maj. Lena Svensson's Private Quarters 40, Security Chief]
    C1 --> C1d[Dr. Hiroshi Tanaka's Private Quarters 50, Geologist]
    C1 --> C1e[Dr. Emily Roche's Private Quarters 34, Astrobiologist]
    C1 --> C1f[Prof. Samuel Ndlovu's Private Quarters 47, Theoretical Physicist]
    C1 --> C1g[Nina Petrova's Private Quarters 29, Robotics Engineer]
    C1 --> C1h[Carlos Rivera's Private Quarters 39, Systems Architect]
    C1 --> C1i[Ling Wei's Private Quarters 42, Environmental Engineer]
    C1 --> C1j[Sarah Al-Hakim's Private Quarters 36, Resource Operations Manager]
    C1 --> C1k[Jackson Miles's Private Quarters 33, Supply Chain Coordinator]
    C1 --> C1l[Sgt. Dmitri Volkov's Private Quarters 37, Tactical Officer]
    C1 --> C1m[Li Mei's Private Quarters 32, Cybersecurity Specialist]
    C1 --> C1n[Dr. Sofia Gonzalez's Private Quarters 41, Chief Medical Officer]
    C1 --> C1o[Jamal Anwar's Private Quarters 28, Culinary Specialist]

    C3 --> C3a[Gym]
    C3 --> C3b[VR Entertainment Suites]
    C3 --> C3c[Zero-Gravity Pool]

    D --> D1[Biology and Life Sciences Lab]
    D --> D2[Physics and Materials Science Lab]
    D --> D3[Geology and Planetary Sciences Lab]
    D --> D4[Engineering and Robotics Workshop]

    E --> E1[Hydroponics and Aquaponics Gardens]
    E --> E2[Water Recycling and Air Purification Systems]
    E --> E3[Food Storage and Preparation Areas]

    F --> F1[Fusion Reactor Core]
    F --> F2[Ion Propulsion Systems]
    F --> F3[Nuclear Propelant Magazine]
    F --> F4[Maintenance and Repair Workshops]
    F --> F5[Nuclear Propelant Pulse Unit Ejector]

    G --> G1[Hangar Bays for Exploration Drones and Shuttles]
    G --> G2[Armory and Security Operations Center]
    G --> G3[Shielding Systems and Defensive Weaponry Controls]"""
    
#The description of the setting and the mission. Part of the prompt
ship_description = """
MISSION BRIEF:
The Harmony of the Spheres, a vessel borne from the merged ambitions
of a Chinese-led coalition with giants like Microsoft and Husqvarna,
heads toward a mysterious wormhole near Uranus. More than a mission
of exploration, it's a pursuit shadowed by the ulterior motives
of power and control, emblematic of a world where corporate and
state powers intertwine ominously.
This spacecraft, powered by nuclear pulse propulsion, embodies the
coalition's dual intent: to discover and to dominate. Its design—a
fortress veiled as a research vessel—hides the true dystopian nature
of its voyage across the void.
The crew, a mosaic of the coalition's hierarchy, operates under a veneer
of professionalism, their true freedom curtailed by constant surveillance
and implicit agendas. The wormhole, while a frontier for science, is eyed
for its strategic potential, making the mission a silent battleground
for influence and supremacy.
Amidst the simulated gravity and semblance of Earth-like conditions, the
crew's existence is marred by the overhang of surveillance and the
simmering tension of hidden objectives. Trust is scarce, with each
discovery potentially serving darker goals beyond mere exploration.
As Harmony advances, the excitement of unearthing cosmic secrets is
overshadowed by the stark reality of its journey—a testament to a
future where discovery is inseparable from the shadow of domination,
and the vastness of space becomes just another arena for dystopian ambitions."""

#concatenated prompt, the map and the description
ship_prompt = ship_description + HTHS


#Different random events for the different parts of the spacecraft
command_module_act = [
    "Strategic mission planning and execution discussions",
    "Navigational strategy meetings and course adjustments",
    "Crisis management and emergency response simulations",
    "Interdepartmental coordination meetings for mission coherence",
    "Quantum communication sessions with Earth for updates and reporting"
]
command_module_act_x = random.choice(command_module_act)

community_act = [
    "Cultural exchange nights and international cuisine evenings",
    "Recreational competitions and team-building games",
    "Mental health circles and stress-relief workshops",
    "Personal reflection and diary recording for historical documentation",
    "Educational workshops on various topics from crew members' expertise"
]
community_act_x = random.choice(community_act)

labs_act = [
    "Collaborative scientific research and discovery sharing sessions",
    "Experimentation with new technologies and theoretical models",
    "Environmental monitoring and sustainability initiative planning",
    "Educational seminars on recent scientific advancements",
    "Data analysis marathons and hypothesis generation meetings"
]
labs_act_x = random.choice(labs_act)

support_sys_act = [
    "Resource allocation discussions and efficiency brainstorming",
    "Hydroponics gardening and botanical experiments",
    "Water and air quality testing and adjustment procedures",
    "Food preparation and culinary experimentation with limited resources",
    "Waste recycling and materials repurposing workshops"
]
support_sys_act_x = random.choice(support_sys_act)

engineering_act = [
    "Maintenance and repair sessions for ship systems",
    "Engineering challenges and troubleshooting meetings",
    "Performance reviews and upgrades of propulsion systems",
    "Robotics programming and drone maintenance workshops",
    "Energy management strategies and nuclear reactor safety drills"
]
engineering_act_x = random.choice(engineering_act)

defense_act = [
    "Security drills and defensive strategy planning",
    "Exploration mission planning and drone piloting training",
    "Armory management and weapons safety courses",
    "Observational astronomy sessions and celestial navigation",
    "Cybersecurity workshops and intrusion detection simulations"
]
defense_act_x = random.choice(defense_act)


# The different parts of the ship, with their events and descriptions
sphere_spine_a = ["⁅◌◌⟪Harmony of the Spheres Spine⟫◌◌⁆", "The central axis of the ship, housing critical systems and providing structural integrity for the spacecraft.", "EVENT FILMED:", command_module_act_x ]
ring_one_c = [ "⁅◌◌⟪Ring One: Living Quarters and Community Spaces⟫◌◌⁆", "A habitat ring with crew quarters, dining areas, and recreational facilities, designed to maintain crew morale and health.", "EVENT FILMED:", community_act_x ]
ring_two_d = [ "⁅◌◌⟪Ring Two: Science and Research Labs⟫◌◌⁆", "Dedicated to scientific discovery and analysis, this ring contains state-of-the-art laboratories for various scientific disciplines.", "EVENT FILMED:", labs_act_x ]
ring_three_e = [ "⁅◌◌⟪Ring Three: Exploration and Defense Systems⟫◌◌⁆", "Focuses on sustainability, featuring systems for hydroponics, recycling, and life support to ensure long-term survivability.", "EVENT FILMED:", support_sys_act_x ]
vertebrae_one_b = [ "⁅◌◌⟪Vertebrae One: Command and Control Module⟫◌◌⁆", "Houses the bridge, navigation, and communications hub, serving as the nerve center for the entire mission", "EVENT FILMED", command_module_act_x ]
vertebrae_two_g = [ "⁅◌◌⟪Vertebrae Two: Exploration and Defense⟫◌◌⁆", "Equipped with hangar bays for drones and shuttles, armories, and defensive systems to protect the ship and support exploration activities.", "EVENT FILMED", defense_act_x ]
vertebrae_three_f = [ "⁅◌◌⟪Vertebrae Three: Propulsion and Engineering⟫◌◌⁆", "Contains the ship's propulsion systems, including the nuclear pulse propulsion mechanism, and engineering workshops for maintenance and repairs.", "EVENT FILMED", engineering_act_x ]
bridge_b1 = [ "⁅◌◌⟪Bridge⟫◌◌⁆", "The nerve center of the Harmony of the Spheres, the Bridge is equipped with state-of-the-art navigation and control systems. Commanded by the mission commander, it provides panoramic views of space and sophisticated interfaces for piloting and monitoring the ship’s vital functions.", "EVENT FILMED", command_module_act_x ]
com_hub_b2 = [ "⁅◌◌⟪Navigation and Communications Hub⟫◌◌⁆", "This area is the operational heart for all navigational and communication activities aboard the ship. It houses advanced systems for deep space communication, stellar navigation, and is the primary location for coordinating the ship's trajectory and maintaining contact with Earth and other vessels.", "EVENT FILMED", command_module_act_x ]
com_array_b3 = [ "⁅◌◌⟪Communication Array Control⟫◌◌⁆", "The Communication Array Control room manages the ship's cutting-edge communication system, enabling lightspeed data transfer across vast distances through advanced laser systems. This ensures the crew can send and receive messages even if they experience severe communication delays. At times even signal misalignment for weeks at a time halting all communications.", "EVENT FILMED", command_module_act_x ]
dinning_c2 = [ "⁅◌◌⟪Communal Dining Area⟫◌◌⁆", "A social space where crew members gather for meals, fostering a sense of community and collaboration.", "EVENT FILMED", community_act_x ]
rec_center_c3 = [ "⁅◌◌⟪Recreational Facilities⟫◌◌⁆", "Includes a gym, VR entertainment suites, and a zero-gravity pool, supporting physical and mental well-being.", "EVENT FILMED", support_sys_act_x ]
medbay_c4 = [ "⁅◌◌⟪Medical Bay⟫◌◌⁆", "A fully equipped medical facility to address the health needs of the crew, from routine check-ups to emergencies.", "EVENT FILMED:", community_act_x ]
gym_c3a = [ "⁅◌◌⟪Gym⟫◌◌⁆", "The Gym is designed to cater to the physical well-being of the crew, equipped with various exercise equipment tailored for use in low-gravity environments. It plays a crucial role in keeping the crew physically healthy and combatting the muscle and bone density loss associated with extended space travel.", "EVENT FILMED", community_act_x ]
vrsuites_c3b = [ "⁅◌◌⟪VR Entertainment Suites⟫◌◌⁆", "These suites offer immersive virtual reality experiences for recreation and relaxation, allowing crew members to escape the confines of the ship and experience simulations of Earth environments, engage in interactive games, or participate in virtual social gatherings.", "EVENT FILMED", community_act_x ]
gravpool_c3c = [ "⁅◌◌⟪Zero-Gravity Pool⟫◌◌⁆", "A unique recreational feature, the Zero-Gravity Pool uses controlled environments to create a weightless swimming experience. It not only serves as a novel relaxation and exercise area but also as a space for crew members to socialize and unwind from the stresses of the mission.","EVENT FILMED", community_act_x ]
biolab_d1 = [ "⁅◌◌⟪Biology and Life Sciences Lab⟫◌◌⁆", "Specializes in the study of alien life forms and ecosystems encountered during the mission.", "EVENT FILMED", labs_act_x ]
physlab_d2 = [ "⁅◌◌⟪Physics and Materials Science Lab⟫◌◌⁆", "Focuses on analyzing physical properties and materials found in space, aiding in technological advancements.", "EVENT FILMED", labs_act_x ]
geolab_d3 = [ "⁅◌◌⟪Geology and Planetary Sciences Lab⟫◌◌⁆", "Dedicated to the study of geological features and processes on celestial bodies, including the Ringworld.", "EVENT FILMED", labs_act_x ]
enginework_d4 = [ "⁅◌◌⟪Engineering and Robotics Workshop⟫◌◌⁆", "Supports the development and maintenance of the ship's robotic systems and engineering projects.", "EVENT FILMED", engineering_act_x ]
garden_e1 = [ "⁅◌◌⟪Hydroponics and Aquaponics Gardens⟫◌◌⁆", "Produces fresh food for the crew, utilizing advanced agricultural techniques in a controlled environment.", "EVENT FILMED", support_sys_act_x ]
recycling_e2 = [ "⁅◌◌⟪Water Recycling and Air Purification Systems⟫◌◌⁆", "Ensures the ship's water and air remain clean and sustainable, critical for long-duration missions.", "EVENT FILMED", support_sys_act_x ]
foodprep_e3 = [ "⁅◌◌⟪Food Storage and Preparation Areas⟫◌◌⁆", "Manages the storage, preparation, and distribution of food, crucial for crew morale and health.", "EVENT FILMED", support_sys_act_x ]
fusion_f1 = [ "⁅◌◌⟪Fusion Reactor Core⟫◌◌⁆", "he primary power source for the ship, providing energy for all systems and operations.", "EVENT FILMED", engineering_act_x ]
ion_f2 = [ "⁅◌◌⟪Ion Propulsion Systems⟫◌◌⁆", "Offers efficient maneuvering in space, complementing the main propulsion system.", "EVENT FILMED", engineering_act_x ]
nuc_f3 = [ "⁅◌◌⟪Nuclear Reactor⟫◌◌⁆", "Stores the nuclear material used for the pulse propulsion system, key to the ship's long-distance travel capabilities.", "EVENT FILMED", engineering_act_x ]
maint_f4 = [ "⁅◌◌⟪Maintenance and Repair Workshops⟫◌◌⁆", "Equipped for ongoing maintenance and repairs, ensuring the ship remains operational throughout its mission.", "EVENT FILMED:", engineering_act_x ]
nuc_eject_f5 = [ "⁅◌◌⟪Nuclear Reactor Ejector⟫◌◌⁆", "The mechanism for the nuclear pulse propulsion system, enabling high-speed travel to distant destinations.", "EVENT FILMED", engineering_act_x ]
hangar_g1 = [ "⁅◌◌⟪Hangar Bays for Exploration Drones and Shuttles⟫◌◌⁆", "Launch and storage areas for drones and shuttles used in exploration and defense operations.", "EVENT FILMED", defense_act_x ]
armory_g2 = [ "⁅◌◌⟪Armory and Security Operations Center⟫◌◌⁆", "Houses weapons and serves as the coordination point for security measures and defensive strategies.", "EVENT FILMED", defense_act_x ]
shield_g3 = [ "⁅◌◌⟪Shielding Systems and Defensive Weaponry Controls⟫◌◌⁆", "Protects the ship from external threats and manages the deployment of defensive systems in case of conflict.", "EVENT FILMED", defense_act_x ]

#A list of the modules for random selection
modules = [ bridge_b1, com_hub_b2, com_array_b3, dinning_c2, rec_center_c3, medbay_c4, gym_c3a, vrsuites_c3b, gravpool_c3c, biolab_d1, physlab_d2, geolab_d3, enginework_d4, garden_e1, recycling_e2, foodprep_e3, fusion_f1, ion_f2, nuc_f3, maint_f4, nuc_eject_f5, hangar_g1, armory_g2, shield_g3]

#A list of probabilities for random selection
probabilities = [0.30, 0.25, 0.25, 0.15]
# Randomly select the number of crew members
num_selected = random.choices(range(4), weights=probabilities)[0]
# Randomly select crew members
selected_crew = random.sample(list(crew_members.keys()), num_selected)
# Join the selected crew members into a string with the selected attributes
selected_crew_info = "\n".join([f"Name: {crew_members[crew_member]['name']} ({crew_members[crew_member]['age']} years old)\nFaction: {crew_members[crew_member]['alliance']}\nDescription: {crew_members[crew_member]['description']}\nPersonality: {crew_members[crew_member]['personality']}\nProfession: {crew_members[crew_member]['profession']}\n\n" for crew_member in selected_crew])
# The final selection of crew members with attributes
#crew_members = selected_crew
# Just the names alias of the crew selected
#selected_crew = crew_members
#Select the module with the event
 
moduleselection= random.choice(modules)
select_module = moduleselection
#selected_module = select_module

JSON = """{
  "Describe an accident/misunderstanding or other unfortunate event": {
    "What happened": "string",
    "How does it go wrong": "string",
    "What are the long-term consequences": "string",
    "Who is to blame": "string"
  },
  "Describe the tension between the crewmembers?": {
    "Who is suspicious of whom?": "string",
    "Are any of them plotting against each other?": "string",
    "Is anyone misunderstanding something?": "string"
    }
}"""
main1 = """
[CONTEXT]
{ship_prompt}
CREW MEMBERS FILMED:
{selected_crew_info}
FILMED IN:
{select_module}.
Your reflections should should be analytical about the events and try 
to answear questions in a shorth and concise way. 
The expeditions has a tense and hostile work enviroment. 
Where the crew has started to distrust members of differnet 
factions and the crew has started to plot against each other.
[IMPORTANT!]
If no crewmember are mentioned at the moment, keep it shorth 
and to the point!"
[TASK]
Your task is to return a JSON object with this structure:
{JSON}
The string should be a reflection on the events filmed in 
real-time onboard the spaceship and the crew of The Heavenly Sphere:
[OUTPUT]"""


#The second prompt for the narration
json_prompt1 = PromptTemplate.from_template(main1)
#The first prompt for reflection

main2 = """"
[TASK]
Your task is to return a JSON object with only an `out_put_string` 
name that is paired with a string that should be a narration of 
events filmed in real-time onboard the spaceship. The string should 
be written in a shorth and modernistic style.
[REFLECTION]
These reflections are meant to help you narrate the events:
{reflection}
[CONTEXT]
{ship_prompt}
CREW MEMBERS FILMED: 
{selected_crew_info}
FILMED IN:
{select_module}.
Your description should be from the perspective of an outside observer watching 
the event onscreen, giving a brief window into the troubled mission. 
The expeditions has a tense and hostile work enviroment. Where the crew 
has started to distrust members of differnet factions and the crew has started 
to plot against each other.
[IMPORTANT!]
If no crewmember are mentioned at the moment, keep it shorth 
and to the point!"
[OUTPUT]"""

json_prompt2 = PromptTemplate.from_template(main2)

#The json parser
json_parser = SimpleJsonOutputParser()

#The model for the first prompt
model1 = KoboldApiLLM(endpoint="https://wall-ride-jobs-semester.trycloudflare.com", max_length= 500, temperature=0.5, )
model2 = KoboldApiLLM(endpoint="https://wall-ride-jobs-semester.trycloudflare.com", max_length= 250, temperature=0.5 )



#The langchain chains
json_chain1 = json_prompt1 | model1
json_chain2 = json_prompt2 | model2


    


# The reflection and the narration call
reflection = json_chain1.invoke({'JSON': JSON, "selected_crew_info": selected_crew_info, "select_module": select_module, "ship_prompt": ship_prompt} )
#
narration = json_chain2.invoke({"reflection": reflection, "ship_prompt": ship_prompt, "selected_crew_info": selected_crew_info, "select_module": select_module})

def survilence_output():
    main = ["CREW MEMBERS FILMED:", str(selected_crew_info), "FILMED IN:", str(select_module), "NARRATION:", str(narration)]
    joined_elements = " ".join(main)
    return joined_elements


from rich.layout import Layout
from rich.panel import Panel
from rich import box
from rich.console import Console

my_console = Console()    
test = survilence_output()
layout = Layout(name="root")
layout["root"].update(
Layout(Panel(test, box=box.ROUNDED, title="◯⁆⁆⫻SURVILENCE FEED⫻⁅⁅◯", subtitle=" [green]Microsoft SoftTouch--The premier employee engagement platform! ", border_style="red")),
        )
my_console.print(layout)