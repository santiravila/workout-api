from fastapi import APIRouter, HTTPException, status
from .dependencies import ServiceDep
from .schemas import RoutineCreate, RoutineRead, RoutineUpdate


router = APIRouter(prefix="/api/v1/routines", tags=["routines"],)


@router.post("/", response_model=RoutineRead)
def create_routine(
    payload: RoutineCreate,
    service: ServiceDep
) -> RoutineRead:
    routine = payload.to_domain()
    saved_routine = service.create_routine(routine=routine)

    return RoutineRead.from_domain(saved_routine)


@router.get("/{routine_id}", response_model=RoutineRead)
def get_routine(
    routine_id: int,
    service: ServiceDep
) -> RoutineRead:
    try:
        routine = service.get_routine(routine_id=routine_id)
        return RoutineRead.from_domain(routine) 
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Not an existing routine of id: {routine_id}"
        )



@router.get("/", response_model=list[RoutineRead])
def get_routines(
    service: ServiceDep
) -> list[RoutineRead]:
    routines = service.list_routines()
    
    return [RoutineRead.from_domain(routine) for routine in routines]


@router.patch("/{routine_id}", response_model=RoutineRead)
def update_routine(
    routine_id: int, 
    payload: RoutineUpdate,
    service: ServiceDep
) -> RoutineRead:
    update_data = payload.model_dump(exclude_unset=True)
    try:
        updated_routine = service.update_routine(routine_id=routine_id, update_data=update_data)
        return RoutineRead.from_domain(updated_routine)
    except ValueError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 
            detail=f"Not an existing routine of id: {routine_id}"
        )




@router.delete("/{routine_id}", response_model=RoutineRead)
def delete_routine(
    routine_id: int,
    service: ServiceDep
) -> RoutineRead:
    try:
        removed_routine = service.delete_routine(routine_id=routine_id)  
        return RoutineRead.from_domain(removed_routine) 
    except ValueError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 
            detail=f"Not an existing routine of id: {routine_id}"
        )
    