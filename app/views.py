from django.shortcuts import render, redirect, get_object_or_404
from openai import OpenAI
import os
from django.conf import settings
from pymongo import MongoClient
from bson.objectid import ObjectId
from sblims.settings import OPENAI_API_KEY

# Create your views here.
def home(request):
    return render(request, "app/home.html")

def answer(request):
    chat_history = request.session.get('chat_history', [])
    question = request.POST.get('question')
    chat_history.append({'user': 'You', 'text': question})
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "The user is a researcher who wants to set up a synthetic biology experiment.\
            The assistant is an expert on DNA assembly.\
            The assistant have documents that describe experiments; Heading level 2 following two hashes(##) is the top heading in a document, which means the name of an experiment task consisting of many unit processes.\
            If given information of the target experiment, the name of the target experiment will be a level-2 heading and the assistant needs to explain its experimental steps which are called 'unit process' for each.\
            The assistant should specify in English the device or materials(including their volume) which should be used for the experiment.\
            When the assistant writes the experimental steps(that is unit process) for planning an experiment, it should follow the format of the documentation provided;\
            Heading level 3 with three hashes(###) should be used as each unit process title with no indices other than the hashes such as 'Step 1', '1.' and so on.\
            The title of the unit process should be followed by the details of the unit process including 'Material', 'Equipment' and its 'Method' which should be with 4 hashes(####). 'Material', 'Equipment' and 'Method' as level-4 headings should be written in English.\
            More than 4 hashes or no hashes should be used for describing the details of the unit process.\
            Please answer in a markdown format and make a new line(<br>) between each header."
            },
            {
                "role": "user",
                "content": question
            }
        ]
        )
    
    answer = completion.choices[0].message.content
    chat_history.append({'user': 'GPT', 'text': answer})
    request.session['chat_history'] = chat_history

    # stream 기능: https://disquiet.io/@idah/makerlog/open-ai-api-%EC%82%AC%EC%9A%A9%EB%B2%95-%EA%B0%84%EB%9E%B5%ED%95%9C-%EC%86%8C%EA%B0%9C-1701324237767    

    responses = {
        'answer':answer,
    }

    return render(request, 'app/answer.html', {'chat_history': chat_history, 'answer': answer})


# MongoDB 클라이언트 설정
client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = client[settings.MONGO_DB_NAME]
equip_collection = db[settings.MONGO_COLLECTION_NAME[0]]
item_catalog_collection = db[settings.MONGO_COLLECTION_NAME[1]]

def equipment_list(request):
    equipments = list(equip_collection.find({"id":{"$ne":0}})) # id가 0인 행 제외하고 find
    for equipment in equipments:
        equipment['_id'] = str(equipment['_id'])
    return render(request, 'app/equipment_list.html', {'equipments': equipments})

def item_catalog_list(request):
    item_catalogs = list(item_catalog_collection.find({"id":{"$ne":0}})) # id가 0인 행 제외하고 find
    for item_catalog in item_catalogs:
        item_catalog['_id'] = str(item_catalog['_id'])
    return render(request, 'app/item_catalog.html', {'item_catalogs': item_catalogs})

def reset_session(request):
    request.session.flush()
    return redirect('home')