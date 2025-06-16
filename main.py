from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {'id': 1, 'title': 'Sochi', 'name':'sochi'},
    {'id': 2, 'title': 'Dubai', 'name':'dubai'},
]

# Принимают query и path параметры (get, delete)
@app.get("/")
def get_hotels(
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

# Принимают body, request body (put, patch, post)
@app.post('/hotels')
def create_hotel(
    title: str = Body(embed=True)
):
    global hotels
    hotels.append({
         'id': hotels[-1]['id'] + 1,
         'title': title
    })
    return {'status': 'OK'}


# Задача 1
# PUT - ручка, клиент обязан отправить все параметры сущности кроме id, меняем только title и name, обязательно принимаем оба эти параметра
@app.put('/hotels/{hotel_id}')
def change_all_hotel_data(
    hotel_id: int,
    title: str = Body(),
    name: str = Body()
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title
            hotel['name'] = name
    return {'status': 'OK'} 

# Задача 2
# PATCH - ручка, клиент обязан отправить все параметры сущности кроме id, меняем либо title, либо name, либо и то, и то, принимаем параметры опционально
@app.patch('/hotels/{hotel_id}')
def change_partly_hotel_data(
    hotel_id: int,
    title: str = Body(None),
    name: str = Body(None)
):
    global hotels
    for hotel in hotels:
        if title and hotel['id'] == hotel_id:
            hotel['title'] = title
        elif name and hotel['id'] == hotel_id:
            hotel['name'] = name
    return {'status': 'OK'} 

# 3 вариант запуска приложения - рекомендуемый (в консоли только python main.py)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)