# API Contract Design (the public interface)

## The models

| Model Name | Inherits From | Fields | Purpose | Validation/Rules |
| :--- | :--- | :--- | :--- | :--- |
| Exercise | BaseModel | name: (str, **required**), sets: (int, **required**), reps: (int, **optional**), weight: (float, kg/lb, **optional**),  duration: (int, seconds, **optional**), | Bundle exercise data and work as a Value Object inside Routines and Sessions aggregate roots | either reps or duration should be used, but neither both or none. sets > 0, reps >= 0 (if selected), duration >= 0 (if selected), name only composed of (a-z, A-Z, _, -, space) |
| RoutineBase | BaseModel | name: (str, **required**), exercises: (list[Exercise], **required**), rest_between_sets: (int, seconds **required**), tempo: (str, **optional**) | Shared fields | name only composed of (a-z, A-Z, _, -, space), tempo is formatted as (a-b-c-d where a,b,c, and d are (1-9)) |
| RoutineCreate | RoutineBase | empty for now | Create a new routine | none for now |
| RoutineRead | RoutineBase | id: (int), created_at: (datetime) | Return the routine to the client | id > 0 |



# The Endpoints

| Action | HTTP Method | Path template | Request Body | Response Model | Logic/Validation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| List all Routines | GET | /routines | None | list[RoutineRead] | Retrieve as JSON all Routines from a JSON. Ensure read Routines fit with the RoutineBase model |
| Get a specific routine | GET | /routines/{routine_id} | None | RoutineRead | Retrive JSON of the routine with ID routine_id in the JSON. Ensure ID is valid and that there is a Routine of that ID at all. Ensure the reponse model RoutineRead fits the Routine JSON |
| Create a Routine | POST | /routines | RoutineCreate | RoutineRead | Write a new entry to the JSON storing the routines based on the Request Body, validate it fits the RoutineCreate model including the list of exercises |
| Update a Routine | PUT | /routines/{routine_id} | RoutineCreate | RoutineRead | Replace the whole Routine with the corrections added |
| Delete a Routine | DELETE | /routines/{routine_id} | None | RoutineRead | Delete a routine by ID | 
