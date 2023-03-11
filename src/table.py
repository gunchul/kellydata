def table_header_gen(headers):
    header_tr = "<tr>\n"
    for header in headers:
        header_tr += f'<th scope="col">{header}</th>\n'
    header_tr += "</tr>\n"
    return header_tr

def table_body_gen(rows):
    body_trs = ""
    for cols in rows:
        body_trs += "<tr>\n"
        for col in cols:
            body_trs += f"<td>{col}</td>\n"
        body_trs += "</tr>\n"
    return body_trs

def table_gen(headers, rows):
    return f'''
    <div class="table-responsive">
    <table class="table table-striped table-sm">
        <thead>
            {table_header_gen(headers)}
        </thead>
        <tbody>
            {table_body_gen(rows)}
        </tbody>
    </table>
    '''

if __name__ == "__main__":
    table = table_gen(["ABC", "DEF"], [["a", "A"],["b", "B"],["c", "C"]])
    print(table)
