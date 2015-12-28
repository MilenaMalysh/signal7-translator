from lexycal_tables import indents, constants
from Tree import Tree, Node
import pickle

class Synt_p(object):
    def __init__(self, tokens,fileout):
        super(Synt_p, self).__init__()
        self.tree = None
        self.token_list = tokens
        self.i = 0
        self.TS = {}
        self.fileout = fileout
        self.lines = []
        self.f=None
        self.label=0

    def writel(self, stringg):
        self.lines.append(stringg)

    def parse(self):
        try:
            self.signal_program().print_tree()
            self.f = open(self.fileout, 'wb')
            #pickle.dump(self.lines, self.f)
            for item in self.lines:
                self.f.write("%s\n" % item)
            self.f.close()
        except Exception as e:
           print e

    def scan(self):
        self.try_lex()
        self.i += 1

    def raise_error(self, node):
        raise Exception("Syntax error in " + node + " in position " + str(self.TS))

    def try_lex(self):
        self.TS = self.token_list[self.i]

    def signal_program(self):
        self.tree =Tree('signal_program')
        self.tree.add_child(self.program())
        return self.tree

    def program(self):
        self.scan()
        if self.TS['id'] != 403:
            self.raise_error('signal_program')
        progr = Node('program')
        progr.add_child('PROGRAM')
        lab_name=self.procedure_identifier()
        progr.add_child(lab_name)
        self.scan()
        if self.TS['body'] != ';':  # Code of ';'
            self.raise_error('program')
        progr.add_child(';')
        progr.add_child(self.block(lab_name))
        try:
            self.scan()
        except:
            print('Syntax error')
        if self.TS['body'] != '.':
            self.raise_error('program')
        progr.add_child('.')
        return progr

    def procedure_identifier(self):
        self.scan()

        if self.TS in indents:  # Something in idents
            procedure_ident=Node(self.TS['body'])
        else:
            self.raise_error('program')
        return procedure_ident

    def block(self,lab_name):
        next_node = self.variable_declaration()
        lab_name=lab_name.value
        bloc = None
        if next_node:
            bloc = Node('bloc')
            bloc.add_child(next_node)
        else:
            self.scan()
        if self.TS['id'] != 401:  # code of BEGIN
            self.raise_error('block')
        if bloc:
            bloc.add_child('BEGIN')
            self.writel(lab_name + ' segment use16')
            self.writel('Assume cs: '+lab_name+', ds: data')
            self.writel('begin:')
            self.writel('mov ax, data')
            self.writel('mov ds, ax')
        else:
            bloc=Node('bloc')
            bloc.add_child('BEGIN')
            self.writel(lab_name+ 'segment use16')
            self.writel('Assume cs: '+lab_name+', ds: data')
            self.writel('begin:')
            self.writel('mov ax, data')
            self.writel('mov ds, ax')
        self.scan()
        if self.TS['id'] == 407:
            bloc.add_child(self.statements_list())
        else:
            self.writel('nop')
        if self.TS['id'] != 402:  # code of END
            self.raise_error('block')
        bloc.add_child('END')
        self.writel('mov ax, 4c00h')
        self.writel('int 21h')
        self.writel(lab_name+' ends')
        self.writel('end begin')
        return bloc

    def variable_declaration(self):
        self.try_lex()
        if self.TS['id'] == 401:  # code of BEGIN
            variable_decl = None
        else:
            if self.TS['id'] != 404:  # code of VAR
                self.raise_error('block')
            self.scan()
            self.writel('Data segment use16')
            next_node = self.declaration_list()
            if next_node:
                variable_decl = Node('variable_decl')
                variable_decl.add_child('VAR')
                variable_decl.add_child(next_node)
            else:
                self.writel('nop')
                #next_node = self.declaration_list()
                variable_decl = Node('variable_decl')
                variable_decl.add_child('VAR')
            self.writel('Data ends')
        return variable_decl

    def declaration_list(self):
        self.scan()
        if self.TS['id'] == 401:  # code of BEGIN
            decl_list = None
        else:
            decl_list=Node('decl_list')
            decl_list.add_child(self.declaration())
            next_node = self.declaration_list()
            if next_node:
                decl_list.add_child(next_node)
        return decl_list

    def declaration(self):
        if self.TS in indents:  # Something in indents
            decl=Node('Declaration')
            attr_name =self.TS['body']
            decl.add_child(attr_name)
        else:
            self.raise_error('declaration')
        self.scan()
        if self.TS['body'] != ':':  # Simbol tochki z tochkoy
            self.raise_error('declaration')
        decl.add_child(':')
        decl.add_child(self.attribute(attr_name))
        self.scan()
        if self.TS['body'] != ';':  # tochka s zapyatoy
            next_node = self.attributes_list(attr_name)
            decl.add_child(next_node)
        if self.TS['body'] != ';':
            self.raise_error('declaration')
        decl.add_child(';')
        return decl

    def attributes_list(self,attr_name):
        att_list = None
        if self.TS['id'] != ord(';'):  # code of tochka z zapyatoy
            self.i -=1
            att_list=Node('attributes_list')
            att_list.add_child(self.attribute(attr_name))
            self.scan()
            next_node = self.attributes_list(attr_name)
            if next_node:
                att_list.add_child(self.attributes_list(attr_name))
        return att_list

    def attribute(self,attr_name):
        self.scan()
        if self.TS['id'] == 410:  # Code of INTEGER"""
            attr=Node('attribute')
            attr.add_child('INTEGER')
            self.writel(attr_name+ ' dw ??')
        elif self.TS['id'] == 411:  # Code of FLOAT"""
            attr=Node('attribute')
            attr.add_child('FLOAT')
        elif self.TS['id'] == 409:  # Code of SIGNAL """
            attr=Node('attribute')
            attr.add_child('SIGNAL')
        elif self.TS['id'] == 412:  # Code of EXT """
            attr=Node('attribute')
            attr.add_child('EXT')
        else:
            self.raise_error('arrribute')
        return attr

    def statements_list(self):
        stat_list = None
        if self.TS['id'] == 407:
            stat_list = Node('statements_list')
            stat_list.add_child(self.statement())
            self.scan()
            next_node = self.statements_list()
            if next_node:
                stat_list.add_child(next_node)
        return stat_list

    def statement(self):
        stat=Node('statement')
        stat.add_child('FOR')
        self.scan()
        if self.TS in indents:  # Ni odnony ident. v tablize"""
            next_node = Node('variable_identifier')
            stat_iter=self.TS['body']
            next_node.add_child(stat_iter)
            stat.add_child(next_node)
        else:
            self.raise_error('statement')
        self.scan()
        if self.TS['id'] == 301:  # Code of := v tablize
            stat.add_child(':=')
        else:
            self.raise_error('statement')
        stat.add_child(self.loop_declaration(stat_iter))
        self.scan()
        if self.TS['id'] == 408:
            stat.add_child('ENDFOR')
        else:
            self.raise_error('statement')
        self.scan()
        if self.TS['body'] == ';':
            stat.add_child(';')
        else:
            self.raise_error('statement')
        return stat

    def loop_declaration(self,stat_iter):
        loop_dec=Node('loop_declaration')
        loop_dec.add_child(self.expression())
        #elf.writel('Mov '+stat_iter+',AX')
        self.scan()
        if self.TS['id'] != 405:  # Code of TO v tabl"""
            self.raise_error('loop declaration')
        loop_dec.add_child('TO')
        loop_dec.add_child(self.expression())
        self.scan()
        if self.TS['id'] != 406:  # Code of DO v tabl"""
            self.raise_error('loop declaration')
        loop_dec.add_child('DO')
        self.try_lex()
        if self.TS['id'] != 408:
            self.i = self.i + 1
            next_node = self.statements_list()
            if next_node:
                loop_dec.add_child(next_node)
                self.i-=1
        return loop_dec

    def expression(self):
        expr=Node('expression')
        expr.add_child(self.multiplier())
        next_node = self.multipliers_list()
        if next_node:
            expr.add_child(next_node)
        return expr

    def multipliers_list(self):
        self.try_lex()
        mult_list = None
        if (self.TS['id'] != 406)and (self.TS['id'] != 405):  # code of DO or TO"""
            self.scan()
            mult_list=Node('multipliers_list')
            mult_list.add_child(self.multiplication_instruction())
            mult_list.add_child(self.multiplier())
            next_node= self.multipliers_list()
            if next_node:
                mult_list.add_child(next_node)
        return mult_list

    def multiplication_instruction(self):
        if (self.TS['body'] != '*') and (self.TS['body'] != '/') and (self.TS['body'] != '&') and (self.TS['id'] != 413):  # lyubomy kody deystviya."""
            self.raise_error('multiplication')
        mult_inst=Node('multiplication_instruction')
        mult_inst.add_child(self.TS['body'])
        return mult_inst

    def multiplier(self):
        self.scan()
        if self.TS in indents:  # Something in indent
            next_node = Node('variable_identifier')
            next_node.add_child(self.TS['body'])
        elif self.TS in constants:  # Something in constants
            next_node = Node('unsigned_integer')
            next_node.add_child(self.TS['body'])
        else:
            self.raise_error('multiplier')
        mult = Node('multiplier')
        mult.add_child(next_node)
        return mult


















