import sqlite3


class TSlipsModel():
    def __init__(self,  con: sqlite3.connect):
        self.cur = con.cursor()

    def insert(self, slips):
        query = """
                    INSERT INTO TRANSACTION_SLIPS(
                        STORE_NAME,
                        TRANSACTION_DESCRIPTION,
                        TRANSACTION_DATE,
                        TRANSACTION_AMOUNT,
                        TRANSACTION_CATEGORY_ID
                    )
                    VALUES(
                        ?,
                        ?,
                        ?,
                        ?,
                        ?
                    )
                """

        self.cur.execute(query, slips)

    def select_sum_amount_group_by_category(self):
        query = """
                    SELECT
                        C.PNAME,
                        SUM(TS.TRANSACTION_AMOUNT)
                    FROM
                        TRANSACTION_SLIPS AS TS
                        INNER JOIN
                            (
                                SELECT
                                    TC.ID,
                                    TPC.ID AS PID,
                                    TPC.NAME AS PNAME
                                FROM
                                    TRANSACTION_CATEGORIES AS TC
                                    INNER JOIN
                                        TRANSACTION_PARENT_CATEGORIES AS TPC
                                    ON  TC.PARENT_CATEGORY_ID = TPC.ID
                            ) AS C
                        ON  TS.TRANSACTION_CATEGORY_ID = C.ID
                    GROUP BY
                        C.PID
                """

        return self.cur.execute(query).fetchall()

    def select_sum_amount_group_by_transaction_date(self):
        query = """
                    SELECT
                        TRANSACTION_DATE, SUM(TRANSACTION_AMOUNT)
                    FROM
                        TRANSACTION_SLIPS
                    GROUP BY
                        TRANSACTION_SLIPS.TRANSACTION_DATE
                """

        return self.cur.execute(query).fetchall()
