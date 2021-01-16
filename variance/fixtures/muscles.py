
# By default these will be given IDs starting at 1 and incrementing each entry.
DEFAULT_MUSCLE_GROUPS = [
# Areas
("Neck", "Muscles in the neck"),            # ID: 1
("Chest", "Muscles in the chest"),          # ID: 2
("Shoulders", "Muscles in the shoulder"),   # ID: 3
("Back", "Muscles in the back"),            # ID: 4
("Biceps", "Muscles in the biceps"),        # ID: 5
("Triceps", "Muscles in the triceps"),      # ID: 6
("Forearms", "Muscles in the forearm"),     # ID: 7
("Abs", "Muscles in the abdominal"),        # ID: 8
("Quads", "Muscles in the quads/thigh"),    # ID: 9
("Glutes", "Muscles in the glutes"),        # ID: 10
("Hamstrings", "Muscles in the hamstrings"),# ID: 11
("Calves", "Muscles in the calves"),        # ID: 12
# Upper or lower
("Upper body", "Muscles in the upper body"),# ID: 13
("Lower body", "Muscles in the lower body"),# ID: 14
# Other groupings
("Arms", "Muscles in the arms"),            # ID: 15
("Legs", "Muscles in the legs")             # ID: 16
]

# tuple format: ("science-name", "short-name", (group id, group id, ...), diagram-id)
# if short-name is left as "", the scientific name will be used instead
DEFAULT_MUSCLES = [
("Omohyoid", "", (1,), 0),
("Sternohyoid", "", (1,), 0),
("Sternocleidomastoid", "", (1,), 0),
("Trapezius", "Traps", (1, 4, 13), 0),
("Pectoralis Major", "Major pec", (2, 13), 0),
("Pectoralis Minor", "Minor pec", (2, 13), 0),
("Anterior Deltoid", "Anterior delt", (3, 13, 15), 0),
("Middle Deltoid", "Middle delt", (3, 13, 15), 0),
("Posterior Deltoid", "Posterior delt", (3, 13, 15), 0),
("Teres Major", "", (4, 13), 0),
("Teres Minor", "", (4, 13), 0),
("Rhomboid Major", "Rhomboid", (4, 13), 0),
("Infraspinatus", "", (4, 13), 0),
("Erector Spinae", "", (4, 13), 0),
("Thoracolumbar Fascia", "Lumbar", (4, 13), 0),
("Latissimus Dorsi", "Lats", (4, 13), 0),
("Brachialis", "", (5, 13, 15), 0),
("Long Biceps Brachii", "Long Bicep", (5, 13, 15), 0),
("Short Biceps Brachii", "Short Bicep", (5, 13, 15), 0),
("Triceps Brachii lateral", "Lateral Tricep", (6, 13, 15), 0),
("Triceps Brachii long", "Long Tricep", (6, 13, 15), 0),
("Brachiradialis", "", (7, 13, 15), 0),
("Exterior Carpi Ulnaris", "", (7, 13, 15), 0),
("Flexor Carpi Ulnaris", "", (7, 13, 15), 0),
("Abdustor Pollicis Longus", "", (7, 13, 15), 0),
("Pronator Teres", "", (7, 13, 15), 0),
("Palmaris Longus", "", (7, 13, 15), 0),
("Extersor Pollicis Brevis", "", (7, 13, 15), 0),
("Extensor Pollicis Longus", "", (7, 13, 15), 0),
("Flexor Carpi Radialis", "", (7, 13, 15), 0),
("Rectus Abdominis", "", (8, 13), 0),
("Tendinous Inscriptions", "", (8, 13), 0),
("External Oblique", "", (8, 13), 0),
("Serratus Anterior", "", (8, 13), 0),
("Sartorius", "", (9, 14, 16), 0),
("Pectineus", "", (9, 14, 16), 0),
("Adductor Longus", "", (9, 14, 16), 0),
("Gracilis", "", (9, 11, 14, 16), 0),
("Tensor Fasciae Latae", "", (9, 14, 16), 0),
("Vastus Medialis", "", (9, 14, 16), 0),
("Vastus Lateralis", "", (9, 14, 16), 0),
("Rectus Femoris", "", (9, 14, 16), 0),
("Gluteus Maximus", "", (10, 14, 16), 0),
("Gluteus Medius", "", (10, 14, 16), 0),
("Iliotibial Band", "", (11, 14, 16), 0),
("Biceps Femoris", "", (11, 14, 16), 0),
("Adductor Magnus", "", (11, 14, 16), 0),
("Semitendinosus", "", (11, 14, 16), 0),
("Semimembranosus", "", (11, 14, 16), 0),
("Soleus", "", (12, 14, 16), 0),
("Gastrocnemius", "", (12, 14, 16), 0),
("Peroneus Brevis", "", (12, 14, 16), 0),
("Flexor Hallucis Longus", "", (12, 14, 16), 0)
]