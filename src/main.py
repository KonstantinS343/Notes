from fastapi import FastAPI


app = FastAPI(title='Notes')


@app.get('/')
def home():
    return "Hi"
