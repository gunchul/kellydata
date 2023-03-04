import datetime

def rba_table(df, output_path):
    html = f'<div class="table-responsive">\n'
    html += f'<table class="table table-striped table-sm">\n'
    html += f'    <thead>\n'
    html += f'    <tr>\n'
    html += f'        <th scope="col">Date</th>\n'
    html += f'        <th scope="col">Rate</th>\n'
    html += f'        <th scope="col">Changed</th>\n'
    html += f'    </tr>\n'
    html += f'    </thead>\n'
    html += f'    <tbody>\n'
    for row in df.values:
        print(row)
        # date = datetime.datetime.strptime(row[0], "%d %b %Y")
        date = row[1].strftime("%Y-%m-%d")
        price = row[2]
        changed_rate = row[3]
        html += f'    <tr>\n'
        html += f'        <td>{date}</td>\n'
        html += f'        <td>{price}</td>\n'
        html += f'        <td>{changed_rate}</td>\n'
        html += f'    </tr>\n'
    html += f'    </tbody>\n'
    html += f'</table>\n'

    with open(output_path, "w") as f:
        f.write(html)

def exchange_table(df, output_path):
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    html = f'<div class="table-responsive">\n'
    html += f'<table class="table table-striped table-sm">\n'
    html += f'    <thead>\n'
    html += f'    <tr>\n'
    html += f'        <th scope="col">Date</th>\n'
    html += f'        <th scope="col">Rate</th>\n'
    html += f'    </tr>\n'
    html += f'    </thead>\n'
    html += f'    <tbody>\n'
    for row in df.values:
        print(row)
        # date = datetime.datetime.strptime(row[0], "%d %b %Y")
        date = row[0]
        price = row[4]
        html += f'    <tr>\n'
        html += f'        <td>{date}</td>\n'
        html += f'        <td>{price:.4f}</td>\n'
        html += f'    </tr>\n'
    html += f'    </tbody>\n'
    html += f'</table>\n'

    with open(output_path, "w") as f:
        f.write(html)
