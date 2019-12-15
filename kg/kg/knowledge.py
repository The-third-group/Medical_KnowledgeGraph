from django.shortcuts import render
import json

def knowledge(request):

    context ={}
    # try:
    #     search_entity(request)
    # except :
    #     return render(request, 'knowledge.html', context)
    return render(request, 'knowledge.html', context)

# relationCountDict = {}
# def sortDict(relationDict):
#     for i in range(len(relationDict)):
#         relationName = relationDict[i]['rel']['type']
#         relationCount = relationCountDict.get(relationName)
#         if (relationCount is None):
#             relationCount = 0
#         relationDict[i]['relationCount'] = relationCount
#
#     relationDict = sorted(relationDict, key=lambda item: item['relationCount'], reverse=True)
#
#     return relationDict
#
#
# def search_entity(request):
#     print('6')
#     ctx = {}
#     # 根据传入的实体名称搜索出关系
#     if request.GET :
#         entity = request.GET['name']
#         db = Neo4j()
#         db.connectDB()
#         entityRelation = db.getEntityRelationbyEntity(entity)
#         if len(entityRelation) == 0:
#             # 若数据库中无法找到该实体，则返回数据库中无该实体
#             ctx = {'title': '<h1>数据库中暂未添加该实体</h1>'}
#             return render(request, 'knowledge.html', {'ctx': json.dumps(ctx, ensure_ascii=False)})
#         else:
#         	#返回查询结果
#         	#将查询结果按照"关系出现次数"的统计结果进行排序
#             entityRelation = sortDict(entityRelation)
#             print(json.dumps(entityRelation, ensure_ascii=False))
#             return render(request, '123.html', {'entityRelation': json.dumps(entityRelation, ensure_ascii=False)})
#     return render(request, "knowledge.html", {'ctx': ctx})