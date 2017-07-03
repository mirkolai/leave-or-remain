import config as cfg
import pymysql
import community # --> http://perso.crans.org/aynaud/communities/
import networkx as nx

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

G=nx.Graph()

cur.execute("SELECT `source`, `target` FROM `user_friends_relation`")
edges=cur.fetchall()
i=len(edges)
for edge in edges:
    i-=1
    if i%10000==0:
        print(str(i))
        print("Number of nodes ",G.number_of_nodes())
        print("Number of edges ",G.number_of_edges())

    cur.execute("SELECT count(*) FROM `user_friends_relation` where target=%s",(edge[1]))
    target=cur.fetchone()
    if target[0]>=10:
        G.add_edge(edge[0],edge[1])

print("Number of nodes ",G.number_of_nodes())
print("Number of edges ",G.number_of_edges())
print(G.is_directed())
partition = community.best_partition(G)
print("Louvain Modularity: ", community.modularity(partition, G))
#print("Louvain Partition: ", partition)

i=len(partition.items())

for key,value in partition.items():
    i-=1
    print(str(i))
    #print(key,value)
    cur.execute(" INSERT INTO "
                " `user_friends_relation_communities`"
                " (`id`, `community`) "
                " VALUES "
                " (%s,%s) on duplicate key update community=%s",(key,value,value))

