from SPARQLWrapper import SPARQLWrapper, JSON
import pymysql
import config as cfg

parties={ "REMAIN" : [
            "Green_Party_of_England_and_Wales",
            "Labour_Party_(UK)",
            "Liberal_Democrats",
            "Plaid_Cymru",
            "Scottish_Green_Party",
            "Alliance_Party_of_Northern_Ireland",
            "Green_Party_in_Northern_Ireland",
            "Sinn_F%C3%A9in",
            "Social_Democratic_and_Labour_Party",
            "Ulster_Unionist_Party",
            "Gibraltar_Social_Democrats",
            "Gibraltar_Socialist_Labour_Party",
            "Liberal_Party_of_Gibraltar"],

          "LEAVE" : [
            "UK_Independence_Party",
            "Democratic_Unionist_Party",
            "People_Before_Profit_Alliance",
            "Traditional_Unionist_Voice"],

          "NEUTRAL" :[
                "Conservative_Party_(UK)"]
    }


def get_sparql_query_result(query):
    sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()


if __name__ == '__main__':

    db = pymysql.connect(host=cfg.mysql['host'], # your host, usually localhost
                 user=cfg.mysql['user'], # your username
                 passwd=cfg.mysql['passwd'], # your password
                 db=cfg.mysql['db'],
                 charset='utf8') # name of the data base

    cur = db.cursor()
    cur.execute('SET NAMES utf8mb4')
    cur.execute("SET CHARACTER SET utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    db.commit()


    for key_stance in parties:

        for party in parties[key_stance]:
            print(party,key_stance)
            query=" PREFIX db: <http://dbpedia.org/resource/>  " \
                  " select ?uri ?name ?surname" \
                  " { " \
                  "   ?uri    dbo:party <http://dbpedia.org/resource/"+party+">." \
                  "   ?uri    foaf:name ?name. " \
                  "   ?uri    foaf:surname ?surname. " \
                  " } "


            print(query)

            results=get_sparql_query_result(query)

            for member in results["results"]["bindings"]:


                cur.execute(" INSERT INTO `resources_politics`(`url`, `alias`, `party`,`stance`) "
                            " VALUES"
                            " (%s,%s,%s,%s) "
                            " ON DUPLICATE KEY UPDATE url=url ",
                            (member["uri"]["value"], member["name"]["value"], party, key_stance )
                            )
                out_file = open("resources/Semantic_resource_politics_"+key_stance+".txt","a")
                out_file.write(member["name"]["value"]+"\n")
                out_file.close()


                out_file = open("resources/Semantic_resource_politics_and_party.txt","a")
                out_file.write(member["name"]["value"]+"\t"+party+"\n")
                out_file.close()

                cur.execute(" INSERT INTO `resources_politics`(`url`, `alias`, `party`, `stance`) "
                            " VALUES"
                            " (%s,%s,%s,%s) "

                            " ON DUPLICATE KEY UPDATE url=url ",
                            (member["uri"]["value"], member["surname"]["value"], party, key_stance  )
                            )
                out_file = open("resources/Semantic_resource_politics_"+key_stance+".txt","a")
                out_file.write(member["surname"]["value"]+"\n")
                out_file.close()

                out_file = open("resources/Semantic_resource_politics_and_party.txt","a")
                out_file.write(member["surname"]["value"]+"\t"+party+"\n")
                out_file.close()