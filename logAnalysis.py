import psycopg2
DB_NAME = "news"

# 1. What are the most popular three articles of all time?
query1 = ("select title , count(*) as num from articles, log where log.path "
          "like concat('%', articles.slug, '%')  and log.status like '%200%' "
          "group by title order by(num) desc limit 3;")
# 2. What are the most popular author of all time?
query2 = ("select name , count(*) as num from articles, authors, log where "
          "log.path like concat('%', articles.slug, '%') and articles.author"
          "= authors.id and log.status like '%200%' group by authors.name "
          "order by(num) desc;")
# 3. On which days did more than 1% of requests lead to errors?
query3 = ("select date(time) as Date, round(sum(case when status not "
          "like'%200%' then 1 else 0 end)*100.0/count(status),2) as "
          "total from log group by Date order by total desc limit 1;")


def run(query):
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(query)
    out = c.fetchall()
    db.close()
    return out


def prints(query1_Out):
    for i in range(0, len(query1_Out)):
        title = query1_Out[i][0]
        views = query1_Out[i][1]
        print ("\t %s -- %d" % (title, views) + " views")
    print("\n")


def prints3(query1_Out):
    for i in range(0, len(query1_Out)):
        title = query1_Out[i][0]
        error = query1_Out[i][1]
        print ("\t %s -- %.2f" % (title, error) + "% error")
    print("\n")


# stores query result
query1_Out = run(query1)
query2_Out = run(query2)
query3_Out = run(query3)

# print formatted output
print("What are the most popular three articles of all time?")
prints(query1_Out)
print("Who are the most popular article authors of all time?")
prints(query2_Out)
print("On which days did more than 1% of requests lead to errors?")
prints3(query3_Out)
