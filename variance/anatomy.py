from enum import Enum

class Muscle(Enum):
    MAJOR_PEC = (0, "Pectoralis Major", ("chest", "upperbody"))
    MINOR_PEC = (1, "Pectoralis Minor", ("chest", "upperbody"))
    ANTERIOR_DELT = (2, "Anterior Deltoids", ("shoulders", "arms", "upperbody"))
    MEDIAL_DELT = (3, "Medial Deltoids", ("shoulders", "arms", "upperbody"))
    POSTERIOR_DELT = (4, "Posterior Deltoids", ("shoulders", "arms", "upperbody"))
    LATERAL_TRI = (5, "Triceps Brachii Lateral", ("triceps", "arms", "upperbody"))
    MEDIAL_TRI = (6, "Triceps Brachii Medial", ("triceps", "arms", "upperbody"))
    LONG_TRI = (7, "Triceps Brachii Long", ("triceps", "arms", "upperbody"))
    SHORT_BICEP = (8, "Biceps Brachii Short", ("biceps", "arms", "upperbody"))
    LONG_BICEP = (9, "Biceps Brachii Long", ("biceps", "arms", "upperbody"))
    FORARMS = (10, "Forarm, etc.", ("forarms", "arms", "upperbody")) # TODO: Does this need broken up into the actual muscles?
    TRAPEZIUS = (11, "Trapezius", ("trapezius", "back", "upperbody"))
    RECTUS_ABS = (12, "Rectus Abdominis", ("abs", "core"))
    EXTERNAL_OBLIQUES = (12, "External Obliques", ("core", "obliques"))
    INTERNAL_OBLIQUES = (13, "Internal Obliques", ("core", "obliques"))
    TRANS_ABS = (14, "Transversus Abdominis", ("core", "abs"))
    GLUTES = (15, "Gluteus Maximus", ("butt", "rear", "legs", "lowerbody", "hamstrings"))
    SEMITENDINOSUS = (16, "Semitendinosus", ("lowerbody", "legs", "hamstrings"))
    BICEPS_FEMORIS = (17, "Biceps Femoris", ("lowerbody", "legs", "hamstrings"))
    SEMIMEMBRANOSUS = (18, "Semimembranosus", ("lowerbody", "legs", "hamstrings"))
    LATERAL_VASTUS = (19, "Vastus Lateralis", ("lowerbody", "legs", "quadriceps"))
    MEDIAL_VASTUS = (20, "Vastus Medialis", ("lowerbody", "legs", "quadriceps"))
    INTERMED_VASTUS = (21, "Vastus Intermedius", ("lowerbody", "legs", "quadriceps"))
    RECTUS_FEMORIS = (22, "Rectus Femoris", ("lowerbody", "legs", "quadriceps"))
    GATROCNEMIUS = (23, "Gatrocnemius", ("lowerbody", "legs", "calves"))
    SOLEUS = (24, "Soleus", ("lowerbody", "legs", "calves"))
    ANTERIOR_TIBIAL = (25, "Tibialis Anterior", ("lowerbody", "legs", "calves"))
    LATS = (26, "Latissimus Dorsi", ("back"))
    ERECT_SPINAE = (27, "Erector Spinae", ("back"))
    RHOMBOID = (28, "Rhomboid", ("back"))
    TERES_MAJOR = (29, "Teres Major", ("back"))

class MuscleGroup(Enum):
    CHEST = (Muscle.MAJOR_PEC, Muscle.MINOR_PEC)
    CORE = (Muscle.RECTUS_ABS, Muscle.TRANS_ABS, Muscle.EXTERNAL_OBLIQUES, Muscle.INTERNAL_OBLIQUES)
    BICEPS = (Muscle.SHORT_BICEP, Muscle.LONG_BICEP)
    TRICEPS = (Muscle.LATERAL_TRI, Muscle.MEDIAL_TRI, Muscle.LONG_TRI)
    DELTOIDS = (Muscle.ANTERIOR_DELT, Muscle.MEDIAL_DELT, Muscle.POSTERIOR_DELT)
    BACK = (Muscle.LATS, Muscle.ERECT_SPINAE, Muscle.RHOMBOID, Muscle.TERES_MAJOR, Muscle.TRAPEZIUS)
    QUADRICEPS = (Muscle.LATERAL_VASTUS, Muscle.MEDIAL_VASTUS, Muscle.INTERMED_VASTUS, Muscle.RECTUS_FEMORIS)
    CALVES = (Muscle.GATROCNEMIUS, Muscle.SOLEUS, Muscle.ANTERIOR_TIBIAL)
    HAMSTRINGS = (Muscle.GLUTES, Muscle.SEMIMEMBRANOSUS, Muscle.BICEPS_FEMORIS, Muscle.SEMITENDINOSUS)

    PECS = CHEST # Alias
    ABS = CORE # Alias

    LEGS = (Muscle.GLUTES, Muscle.SEMITENDINOSUS, Muscle.BICEPS_FEMORIS, Muscle.SEMIMEMBRANOSUS, Muscle.LATERAL_VASTUS, Muscle.MEDIAL_VASTUS, Muscle.INTERMED_VASTUS, Muscle.RECTUS_FEMORIS, Muscle.GATROCNEMIUS, Muscle.SOLEUS, Muscle.ANTERIOR_TIBIAL)

    #NOTE: UPPER_BODY does not include CORE or BACK!
    UPPER_BODY = (Muscle.MAJOR_PEC, Muscle.MINOR_PEC, Muscle.SHORT_BICEP, Muscle.LONG_BICEP, Muscle.LATERAL_TRI, Muscle.MEDIAL_TRI, Muscle.LONG_TRI, Muscle.ANTERIOR_DELT, Muscle.MEDIAL_DELT, Muscle.POSTERIOR_DELT)
    LOWER_BODY = (Muscle.LATERAL_VASTUS, Muscle.MEDIAL_VASTUS, Muscle.INTERMED_VASTUS, Muscle.RECTUS_FEMORIS, Muscle.GATROCNEMIUS, Muscle.SOLEUS, Muscle.ANTERIOR_TIBIAL, Muscle.GLUTES, Muscle.SEMIMEMBRANOSUS, Muscle.BICEPS_FEMORIS, Muscle.SEMITENDINOSUS)
