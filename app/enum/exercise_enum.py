from enum import Enum as ExerciseEnum

# Defining an enumeration class for Indoor and Outdoor exercise types
class IndoorOutdoorExerciseType(ExerciseEnum):
    indoors = "indoors"
    outdoors = "outdoors"

# Defining an enumeration class for Major, Minor, and Common exercise types
class MajorMinorExerciseType(ExerciseEnum):
    mazor = "mazor"
    minor = "minor"
    common = "common"

# Defining an enumeration class for Measurement types
class MeasurementType(ExerciseEnum):
    count = "count"
    time = "time"

    