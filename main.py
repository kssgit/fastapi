from enum import Enum
from typing import Union
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# 경로 매개변수 
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

## 사전 정의 값
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

## 경로 변환기
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path} 

# 쿼리 매개변수
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items2/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

## Union을 활용한 선택적 매개변수
@app.get("/items2/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


## 여러 경로 매개변수
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/items3/{item_id}")
async def read_user_item(item_id: str, needy: str): # default 값을 명시 하지 않을 경우 필수값으로 인식
    item = {"item_id": item_id, "needy": needy}
    return item

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)