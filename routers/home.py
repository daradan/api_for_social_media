from fastapi import APIRouter

router = APIRouter(tags=['Home Page'])


@router.get('/')
def get_home_page():
    return {'message', 'This is the Home Page'}
