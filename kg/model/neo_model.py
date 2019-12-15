from py2neo import Graph, Node, Relationship, cypher, Path
import neo4j


class Neo4j():
    graph = None

    def __init__(self):
        print("create neo4j class ...")

    def connectDB(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="123123")

    def matchItembyTitle(self, value):

        sql = "MATCH (n:Item { title: '" + str(value) + "' }) return n;"
        answer = self.graph.run(sql).data()
        return answer

    # 根据title值返回互动百科item
    def matchHudongItembyTitle(self, value):
        sql = "MATCH (n:HudongItem { title: '" + str(value) + "' }) return n;"
        try:
            answer = self.graph.run(sql).data()
        except:
            print(sql)
        return answer

    # 根据entity的名称返回关系
    def getEntityRelationbyEntity(self, value):  # title
        answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" + str(
            value) + "\" RETURN rel,entity2").data()
        return answer

    '''
    关系查询   下面
    '''

    # 查找entity1及其对应的关系（与getEntityRelationbyEntity的差别就是返回值不一样）
    def findRelationByEntity(self, entity1):
        # title
        answer = self.graph.run("MATCH (n1 {name:\"" + str(entity1) + "\"})- [rel] -> (n2) RETURN n1,rel,n2").data()
        # if(answer is None):
        # 	answer = self.graph.run("MATCH (n1:NewNode {title:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
        return answer

    # 查找entity2及其对应的关系
    def findRelationByEntity2(self, entity1):  # title
        answer = self.graph.run("MATCH (n1)- [rel] -> (n2 {name:\"" + str(entity1) + "\"}) RETURN n1,rel,n2").data()

        # if(answer is None):
        # 	answer = self.graph.run("MATCH (n1)- [rel] -> (n2:NewNode {title:\""+entity1+"\"}) RETURN n1,rel,n2" ).data()
        return answer

    # 根据entity1和关系查找enitty2
    def findOtherEntities(self, entity, relation):
        # title                                #type
        answer = self.graph.run("MATCH (n1 {name:\"" + str(entity) + "\"})- [rel {name:\"" + str(
            relation) + "\"}] -> (n2) RETURN n1,rel,n2").data()
        # if(answer is None):
        #	answer = self.graph.run("MATCH (n1:NewNode {title:\"" + entity + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2) RETURN n1,rel,n2" ).data()

        return answer

    # 根据entity2和关系查找enitty1
    def findOtherEntities2(self, entity, relation):  # type                                 #title
        answer = self.graph.run("MATCH (n1)- [rel {name:\"" + str(relation) + "\"}] -> (n2 {name:\"" + str(
            entity) + "\"}) RETURN n1,rel,n2").data()
        # if(answer is None):
        #	answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:NewNode {title:\"" + entity + "\"}) RETURN n1,rel,n2" ).data()

        return answer

    # 根据两个实体查询它们之间的最短路径
    def findRelationByEntities(self, entity1, entity2):
        # HudongItem  title         acompany_with                              title
        answer = self.graph.run("MATCH (p1:Disease {name:\"" + str(entity1) + "\"}),(p2:Disease{name:\"" + str(
            entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN rel").evaluate()
        # answer = self.graph.run("MATCH (p1:HudongItem {name:\"" + entity1 + "\"})-[rel:RELATION]-(p2:HudongItem{title:\""+entity2+"\"}) RETURN p1,p2").data()

        if (answer is None):
            answer = self.graph.run("MATCH (p1:Disease {name:\"" + str(entity1) + "\"}),(p2:Disease {name:\"" + str(
                entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
        if (answer is None):
            answer = self.graph.run("MATCH (p1:Disease {name:\"" + str(entity1) + "\"}),(p2:Disease{name:\"" + str(
                entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
        if (answer is None):
            answer = self.graph.run("MATCH (p1:Disease {name:\"" + str(entity1) + "\"}),(p2:Disease {name:\"" + str(
                entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
        # answer = self.graph.data("MATCH (n1:HudongItem {title:\"" + entity1 + "\"})- [rel] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        # if(answer is None):
        #	answer = self.graph.data("MATCH (n1:HudongItem {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        # if(answer is None):
        #	answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        # if(answer is None):
        #	answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        relationDict = []
        if (answer is not None):
            for x in answer:
                tmp = {}
                start_node = x.start_node
                end_node = x.end_node
                tmp['n1'] = start_node
                tmp['n2'] = end_node
                tmp['rel'] = x
                relationDict.append(tmp)
        return relationDict

    # 查询数据库中是否有对应的实体-关系匹配
    def findEntityRelation(self, entity1, relation, entity2):
        # HudongItem  title                                        type								HudongItem  title
        answer = self.graph.run("MATCH (n1:Disease {name:\"" + str(entity1) + "\"})- [rel:RELATION {name:\"" + str(
            relation) + "\"}] -> (n2:Disease{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (answer is None):
            answer = self.graph.run("MATCH (n1:Disease {name:\"" + str(entity1) + "\"})- [rel:RELATION {name:\"" + str(
                relation) + "\"}] -> (n2:Disease{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (answer is None):
            answer = self.graph.run("MATCH (n1:Disease {name:\"" + str(entity1) + "\"})- [rel:RELATION {name:\"" + str(
                relation) + "\"}] -> (n2:Disease{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (answer is None):
            answer = self.graph.run("MATCH (n1:Disease {name:\"" + str(entity1) + "\"})- [rel:RELATION {name:\"" + str(
                relation) + "\"}] -> (n2:Disease{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        return answer

