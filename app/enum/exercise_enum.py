from enum import Enum as ExerciseEnum


class IndoorOutdoorExerciseType(ExerciseEnum):
    indoors = "indoors"
    outdoors = "outdoors"

class MajorMinorExerciseType(ExerciseEnum):
    mazor = "mazor"
    minor = "minor"
    common = "common"

class MeasurementType(ExerciseEnum):
    count = "count"
    time = "time"

    