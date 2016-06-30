import os
import time
from timeit import default_timer as timer
from PIL import Image, ImageDraw, ImageFont

global cellWidth
global cellHeight
global img
global Y
global extensions
global Height

cellWidth = 100
cellHeight = 25
Y = 100
extenstions = {"png": "cyan",
               "jpeg": "cyan",
               "PNG": "cyan",
               "JPEG": "cyan",
               "jpg": "cyan",
               "mkv": "magenta",
               "mp4": "magenta",
               "mpeg": "magenta",
               "docx": "blue",
               "xlsx": "green",
               "pdf": "red",
               "pptx": "orange",
               "vhd": "crimson",
               "py": "purple",
               "java": "violet",
               "class": "violet",
               "zip": "black",
               "txt": "coral"}
Height = 0


class Tree:
    def __init__(self, name, path, contents, Xcor, Ycor):
        self.name = name
        self.path = path
        self.contents = contents


class Leaf:
    def __init__(self, name, path, Xcor, Ycor):
        self.name = name
        self.path = path


class listLeaf:
    def __init__(self, List, Xcor, Ycor):
        self.List = List


def relPath(absPath):
    return absPath.split("\\")[-1]


def prev(path):
    '''returns path one level higher than current'''
    print(path)
    if len(path.split("\\")) > 1:
        List = path.split("\\")
        List = List[:-1]
        Path = ""
        for folder in List[:-1]:
            Path += folder + "\\"
        Path += List[-1]
        return Path
    else:
        pass


def isLeaf(Path):
    return os.path.isfile(Path)


def createTree(path):
    # if "'" in path:
    #    print("\n\n\n",path,"\n\n\n")
    # if leaf node
    if os.path.isdir(path) == False:
        return
    if isLeaf(path):
        return Leaf(relPath(path), os.path.abspath(path), 0, 0)
    else:
        tree = Tree(str(relPath(path)), os.path.abspath(path), [], 0, 0)
        os.chdir(path)
        leaves = []
        for d in os.listdir():
            if isLeaf(d):
                leaves += [Leaf(relPath(d), os.path.abspath(d), 0, 0)]
                pass
            else:
                newDir = path + "\\" + d
                tree.contents += [createTree(newDir)]
        tree.contents += [listLeaf(leaves, 0, 0)]
    return tree


def width(tree):
    w = 0
    for i in tree.contents:
        if isinstance(i, list):
            w += 1
        elif isinstance(i, Tree):
            w += width(i)

    return w


'''
def heightHelper(tree, h):
    #basecase
    if len(tree.contents) ==1 and isinstance(tree.contents[0],list):
        return len(tree.contents[0])

    for c in tree.contents:
        if isinstance(c, list):
            h+=1

    L = []
    for d in tree.contents:
        if isinstance(d, Tree):
            L+=[heightHelper(d, h)]

    for e in tree.contents:
        if isinstance(e, Tree):
            if height(e) == max(L):
                return heightHelper(e, h)

def height(tree):
    return heightHelper(tree,1)
'''


def depth(obj, tree):
    return len(obj.path.split("\\")) - len(tree.path.split("\\"))


def printTreeHelper(branch, tree):
    if isinstance(branch, listLeaf):
        for i in branch.List:
            # print("   "*depth(i, tree) + str(depth(i,tree)))
            print(depth(i, tree), "    " * (depth(i, tree)) + relPath(i.path))
    elif isinstance(branch, Tree):
        # print("    "*depth(branch, tree) + str(depth(branch,tree)))
        print(depth(branch, tree), "    " * depth(branch, tree) + branch.name)
        for c in branch.contents:
            printTreeHelper(c, tree)


def printTree(tree):
    printTreeHelper(tree, tree)


def textOutput():
    path = "C:\\Users\\Lord Daniel\\Desktop\\files"  # \\Uni Stuff\\Spring 2015-2016

    start = timer()
    T = createTree(path)
    end = timer()
    time = (end - start)

    print("PATH: ", path, "\n")
    print("Time to create tree: ", time, "\n")
    print("Width: ", width(T), "\n")
    print("Height: ", height(T), "\n")
    print("Time to create tree: ", time, "\n")

    printTree(T)


def drawTreeImage(branch, tree, img):
    global cellWidth
    global cellHeight
    global Y
    global Font
    global extenstions

    if isinstance(branch, listLeaf):
        for i in branch.List:
            color = None
            if i.name.split(".")[-1] in extenstions:
                color = extenstions[i.name.split(".")[-1]]
            else:
                color = "black"
            X = 100 + 100 * (depth(i, tree))
            cellWidth = 100.0 * len(relPath(i.path)) / 12.0
            img.polygon(((X, Y), (X + cellWidth, Y), (X + cellWidth, Y + cellHeight), (X, Y + cellHeight), (X, Y)),
                        fill=color)
            img.line(((X, Y), (X + cellWidth, Y), (X + cellWidth, Y + cellHeight), (X, Y + cellHeight), (X, Y)),
                     fill="black", width=3)
            img.text((X + 7, Y + 7), relPath(i.path), fill="white")
            Y += cellHeight + 20
    elif isinstance(branch, Tree):
        X = 100 + 100 * (depth(branch, tree))
        cellWidth = 100.0 * len(branch.name) / 12.0
        img.polygon(((X, Y), (X + cellWidth, Y), (X + cellWidth, Y + cellHeight), (X, Y + cellHeight), (X, Y)),
                    fill="grey")
        img.line(((X, Y), (X + cellWidth, Y), (X + cellWidth, Y + cellHeight), (X, Y + cellHeight), (X, Y)),
                 fill="black", width=3)
        img.text((X + 7, Y + 7), branch.name, fill="white")
        Y += cellHeight + 20
        for c in branch.contents:
            drawTreeImage(c, tree, img)


def createTreeImage(tree):
    global img

    im = Image.new('RGBA', (5000, height(tree)), 'white')
    img = ImageDraw.Draw(im)
    drawTreeImage(tree, tree, img)
    im.save(
        "C:\\Users\\Lord Daniel\\Desktop\\files\\Documents\\Python stuff\\Projects\\directory_tree\\" + tree.name + "_tree.png")


def heightHelper(branch, tree):
    global Height
    if isinstance(branch, listLeaf):
        for i in branch.List:
            Height += 1
    elif isinstance(branch, Tree):
        Height += 1
        for c in branch.contents:
            heightHelper(c, tree)


def height(tree):
    global Height
    global cellHeight
    heightHelper(tree, tree)
    return 200 + (cellHeight + 20) * Height


def main():
    path = "C:\\Users\\Lord Daniel\\Desktop\\files"  # \\Spring 2015-2016
    tree = createTree(path)

    start = timer()
    tree = createTree(path)
    end = timer()
    time = (end - start)
    print("PATH: ", path, "\n")
    print("Time to create tree: ", time, "\n")
    printTree(tree)
    '''
    start = timer()
    createTreeImage(tree)
    end = timer()
    time = (end - start)
    print("\nTime to create image: ",time)
    '''


main()


