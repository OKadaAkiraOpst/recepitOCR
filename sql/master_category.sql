-- SQLite
select
tc.ID as 'カテゴリID',
tc.NAME as 'カテゴリ名',
tpc.ID as '親カテゴリID',
tpc.NAME as '親カテゴリ名'
from
TRANSACTION_CATEGORIES tc
inner join
TRANSACTION_PARENT_CATEGORIES tpc
on
tc.PARENT_CATEGORY_ID = tpc.ID
order by tc.ID;