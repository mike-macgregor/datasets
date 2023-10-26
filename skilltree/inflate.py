import csv, json, os

def load_csv(file):
    with open (file) as f:
        reader = csv.reader(f)
        return [row for row in reader]

def map_toDict(list, id='root', useid = True):
    cols = list[0]
    result = {'children':[]}
    if useid : result['id'] = id

    for i in range(1,len(list)-1):
        result['children'].append(
            dict(zip(cols, list[i]))
        )
    return result
def get_children(node, name='children'):
    result = node.get(name)
    if result == None:
        node[name]=[]
        result = node.get(name)
    return result

def inflate_tree(tree):
    children = tree.get('children')
    if children == None: return tree

    for child in children:
        fname = f'{path}{child["id"]}.csv'
        if os.path.isfile(fname) != True: continue
        nx = map_toDict(load_csv(fname),child["id"],useid=False)
        branch = inflate_tree(nx)
        children_of = get_children(child)
        children_of.extend(branch.get('children'))

    return tree

path = 'skilltree/'
rootfile = f'{path}domains.csv'
root = map_toDict(load_csv(rootfile))

tree = inflate_tree(root)
with open(f'{path}skillTree.json', "w") as put:
    put.write(json.dumps(tree, indent=4))
pass