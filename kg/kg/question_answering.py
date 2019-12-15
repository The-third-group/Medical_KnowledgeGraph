from django.shortcuts import render
from py2neo import Graph

def qa(request):
	context = {'ctx': ''}
	graph = Graph("http://localhost:7474", username='neo4j', password='123123')
	print(request)
	if (request.GET):
		question = request.GET['question']
		questions = ''
		for i in range(len(question)):
			if question[i] == '怎':
				break
			else:
				questions = questions + question[i]
		context['answer'] = graph.data('match(n:Disease{name:"' + questions + '"}) return n.cause')

		if context['answer'] == []:
			context['answer'] = '数据库中未找到该内容！'
			return render(request, 'QA.html', context)
		#n.cause
		context['answer'] = context['answer'][0]['n.cause']
	return render(request, 'QA.html', context)