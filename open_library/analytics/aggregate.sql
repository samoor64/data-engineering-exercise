with books_metrics as (
select
    auth.author_key,
    auth.name as author,
    bk.first_publish_year as publish_year,
    count(distinct auth.author_key) over (partition by auth.author_key, bk.first_publish_year) as book_count_by_publish_year
from db.schema.authors as auth
    inner join db.schema.books as bk
        on auth.author_key = bk.author_key
)
select
    author_key,
    author,
    year_written,
    publish_year,
    book_count_by_publish_year,
    avg(book_count_by_publish_year) over (partition by author_key)
from books_metrics
order by author, publish_year