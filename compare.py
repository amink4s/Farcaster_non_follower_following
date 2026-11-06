import duckdb

# result = duckdb.sql("select count(*) from 'followers.csv'")
# print(result)

duckdb.sql("""SELECT fi.username, fi.display_name
FROM read_csv('following.csv') as fi
LEFT JOIN read_csv('followers.csv') as fr
    ON fi.fid = fr.fid
WHERE fr.fid is NULL
""").write_csv('out.csv')