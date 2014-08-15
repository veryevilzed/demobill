
import bottle



app = bottle.Bottle()
plugin = bottle.ext.sqlite.Plugin(dbfile=':memory:')
app.install(plugin)

def __init__(self):
    pass

@app.route('/billing/go')
def go(item, db):
    row = db.execute('SELECT * from items where name=?', item).fetchone()
    if row:
        return template('showitem', page=row)
    return HTTPError(404, "Page not found")





