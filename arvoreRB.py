class Node:
    def __init__(self, data, color=None):
        self.data = data
        self.right = None
        self.left = None
        self.father = None
        self.color = color

    def __str__(self):
        return str(self.data)


class Binarytree:
    def __init__(self):
        self.root = None

    def inorder(self, node=None):
        if self.root is None:
            return None
        if node is None:
            node = self.root
        if node.left:
            self.inorder(node.left)
        if node.data is not None:
            print(node, end=' ')
        if node.right:
            self.inorder(node.right)

    def search(self, x):
        node = self.root
        if node is None:
            return None
        while node != x and node.data is not None:
            if x == node.data:
                return node
            if x < node.data:
                node = node.left
            else:
                node = node.right
        return None

    def minimum(self, node):
        if node is None:
            return None
        dad = node
        while node.left is not None:
            dad = node
            node = node.left
        return dad

    def maximum(self, node):
        if node is None:
            return None
        dad = node
        while node.right is not None:
            dad = node
            node = node.right
        return dad

    def insert(self, x):
        new = Node(x)
        if self.root is None:
            void = Node(None, 'black')
            void.left, void.right = new, new
            new.color = 'black'
            self.root = new
            return
        node = self.root
        while node is not None and node.data is not None:
            dad = node
            if new.data < node.data:
                node = node.left
            else:
                node = node.right
        new.father = dad
        if new.data < dad.data:
            dad.left = new
        else:
            dad.right = new
        new.left = Node(None, 'black')
        new.right = Node(None, 'black')
        new.color = 'red'
        self.insert_fix(new)

    def insert_fix(self, x):
        while x.father.color == 'red':
            if x.father == x.father.father.left:
                y = x.father.father.right
                if y.color == 'red':
                    x.father.color = 'black'
                    y.color = 'black'
                    x.father.father.color = 'red'
                    x = x.father.father
                else:
                    if x == x.father.right:
                        x = x.father
                        self.l_rotate(x)
                    x.father.color = 'black'
                    x.father.father.color = 'red'
                    self.r_rotate(x.father.father)
            else:
                y = x.father.father.left
                if y.color == 'red':
                    x.father.color = 'black'
                    y.color = 'black'
                    x.father.father.color = 'red'
                    x = x.father.father
                else:
                    if x == x.father.left:
                        x = x.father
                        self.r_rotate(x)
                    x.father.color = 'black'
                    x.father.father.color = 'red'
                    self.l_rotate(x.father.father)
            if x.father is None:
                break
        self.root.color = 'black'

    def successor(self, x):
        cur = self.search(x)
        if cur is None:
            return None
        if cur.right is not Node(None):
            succ = self.minimum(cur.right)
            return succ
        succ = cur.father
        while succ is not Node(None) and cur == succ.right:
            cur = succ
            succ = succ.father
        return succ

    def predecessor(self, x):
        cur = self.search(x)
        if cur is None:
            return None
        if cur.left is not Node(None):
            pred = self.maximum(cur.left)
            return pred
        pred = cur.father
        while pred is not Node(None) and cur == pred.left:
            cur = pred
            pred = pred.father
        return pred

    def trasplant(self, dad, son):
        if dad.father == Node(None):
            self.root = son
        elif dad == dad.father.left:
            dad.father.left = son
        else:
            dad.father.right = son
        son.father = dad.father

    def remove(self, r):
        r = self.search(r)
        if r is None:
            return print('elemento nao está na arvore')
        aux = r
        aux_o_color = aux.color
        if self.root is None or r is None:
            print('item ou arvore nao existe')
            return None
        if r.left == Node(None):
            son = r.right
            self.trasplant(r, r.right)
        elif r.right is Node(None):
            son = r.left
            self.trasplant(r, r.left)
        else:
            aux = self.minimum(r.right)
            aux_o_color = aux.color
            son = aux.right
            if aux.father == r:
                son.father = aux
            else:
                self.trasplant(aux, aux.right)
                aux.right = r.right
                aux.right.father = aux
            self.trasplant(r, aux)
            aux.left = r.left
            aux.left.father = aux
            aux.color = r.color
        if aux_o_color == 'black':
            self.delete_fix(r)
        print('item removido')

    def delete_fix(self, r):
        while r != self.root and r.color == 'black':
            if r.father.left == r:
                aux = r.father.right
                if aux.color == 'red':
                    aux.color = 'black'
                    r.father.color = 'red'
                    self.l_rotate(r.father)
                    aux = r.father.right
                if aux.left.color == 'black' and aux.right.color == 'black':
                    aux.color = 'red'
                else:
                    if aux.right.color == 'black':
                        aux.left.color = 'black'
                        aux.color = 'red'
                        self.r_rotate(aux)
                        aux = r.father.right
                    aux.color = r.father.color
                    r.father.color = 'black'
                    aux.right.color = 'black'
                    self.l_rotate(r.father)
                    r = self.root
            else:
                aux = r.father.left
                if aux.color == 'red':
                    aux.color = 'black'
                    r.father.color = 'red'
                    self.r_rotate(r.father)
                    aux = r.father.left
                if aux.left.color == 'black' and aux.right.color == 'black':
                    aux.color = 'red'
                else:
                    if aux.left.color == 'black':
                        aux.right.color = 'black'
                        aux.color = 'red'
                        self.l_rotate(aux)
                        aux = r.father.left
                    aux.color = r.father.color
                    r.father.color = 'black'
                    aux.left.color = 'black'
                    self.r_rotate(r.father)
                    r = self.root
        r.color = 'black'

    def l_rotate(self, x):
        rson = x.right
        if rson.left is not None:
            x.right = rson.left
            rson.left.father = x
        rson.father = x.father
        if x == x.father.right:
            x.father.right = rson
        elif x == x.father.left:
            x.father.left = rson
        else:
            self.root = rson
        rson.left = x
        x.father = rson

    def r_rotate(self, x):
        lson = x.left
        if lson.right is not None:
            x.left = lson.right
            lson.right.father = x
        lson.father = x.father
        if x == x.father.right:
            x.right.father = lson
        elif x == x.father.left:
            x.father.left = lson
        else:
            self.root = lson
        lson.right = x
        x.father = lson


if __name__ == "__main__":
    Tree = Binarytree()
    menu = 1
    print('='*32)
    print('Opçao 1: inserir')
    print('Opcao 2: mostrar em ordem')
    print('opcao 3: minimo e maximo')
    print('opçao 4: sucessor e predecessor')
    print('opcao 5: buscar')
    print('opçao 6: remover')
    print('opçao 0: sair')
    while menu != 0:
        print('='*32)
        menu = input('ESCOLHA A OPÇAO: ')
        print('='*32)
        if menu == '1':
            x = int(input('item a ser inserido: '))
            Tree.insert(x)
            print('item inserido')
        if menu == '2':
            print('Arvore em ordem:', end=' ')
            Tree.inorder()
            print('')
        if menu == '3':
            print('Minimo:', Tree.minimum(Tree.root))
            print('Maximo:', Tree.maximum(Tree.root))
        if menu == '4':
            x = int(input('item a ser rodeado: '))
            print('sucessor:', Tree.successor(x))
            print('predecessor:', Tree.predecessor(x))
        if menu == '5':
            x = int(input('item a ser procurado: '))
            print(Tree.search(x))
        if menu == '6':
            x = int(input('item a ser removido: '))
            Tree.remove(x)
        if menu == '0':
            print('testes completos')
            break

