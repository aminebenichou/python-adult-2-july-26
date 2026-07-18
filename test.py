from manageDb import editRow, createDb
conn = createDb()
editRow(
    conn,
    {
        'desc':'testing update',
        'status': 'Completed'
    },
    5
)