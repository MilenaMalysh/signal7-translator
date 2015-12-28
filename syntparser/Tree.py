# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self, value):
        self.value = value
        self.children = []

    def __contains__(self, item):
        return item == self.value or any(item in child for child in self.children)

    def add_child(self, value):
        if isinstance(value, Node):
            self.children.append(value)
        else:
            self.children.append(Node(value))
        return self.children[-1]

    def __getitem__(self, item):
        if self.value == item:
            return self
        else:
            for child in self.children:
                elem = child[item]
                if elem:
                    return elem

    def find_in_children(self, item):
        if self.children:
            for child in self.children:
                    elem = child[item]
                    if elem:
                        return elem

    def __iter__(self):
        return self.children.__iter__()

    def print_node(self, depth):
        for child in self.children[:-1]:
            if child.value:
                if depth > 0:
                    #print reduce(lambda a, b: a + '│'+' '*3, range(1, depth / 4), ' ' * 4)+'├──'+child.value
                    print reduce(lambda a, b: a + '.'+' '*3, range(1, depth / 4), ' ' * 4)+'├->'+child.value
                else:
                    #print '├──' + child.value
                    print '├->' + child.value
                child.print_node(depth+4)
        if self.children and self.children[-1].value:
            if depth > 0:
                #print reduce(lambda a, b: a + '│' + ' '*3, range(1, depth / 4), ' ' * 4) + '└──'+self.children[-1].value
                print reduce(lambda a, b: a + '.' + ' '*3, range(1, depth / 4), ' ' * 4) + '└->'+self.children[-1].value
            else:
                #print '└──'+self.children[-1].value
                print '└->'+self.children[-1].value
            self.children[-1].print_node(depth+4)

    def pop(self):
        if self.children:
            del self.children[-1]


class Tree(Node):
    def __init__(self, value):
        super(Tree, self).__init__(value)

    def print_tree(self):
        print self.value
        self.print_node(0)

    def __iter__(self):
        return self.children