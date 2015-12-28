

class SemanParser(object):
    def __init__(self, tree):
        self.tree = tree
        self.for_counter = 0
        self.text = ""
        self.error = None
        self.table=[]

    def parse(self):
        try:
            self.text = self.signal_program(self.tree["signal_program"])
        except SemanException as e:
            self.error = e


    def signal_program(self, token):
        return "\n"+self.variable_declaration(token["variable_decl"])+\
               token["program"].children[1].value+ " segment use16\nAssume cs: " +token["program"].children[1].value+", ds: data\n"+ self.block(token["bloc"]) + token["program"].children[1].value+ " ends\nend begin"

    def variable_declaration(self, token):
        if  not token:
            return ""
        else:
            return "Data segment use16\n" + self.decl_list(token["decl_list"]) +"Data ends\n"

    def decl_list(self, token):
        if not token:
            return ""
        else:
            if token["Declaration"].children[0].value in self.table:
                raise Exception("This identifier is already defined")
            else:
                if token["Declaration"].children[2].children[0].value=="INTEGER":
                    self.table.append(token["Declaration"].children[0].value)
        return token["Declaration"].children[0].value + (" df" if token["Declaration"].children[2].children[0].value=="FLOAT" else " dw" ) + "??\n" + self.decl_list(token.find_in_children("decl_list"))

    def block(self, token):
        return "$begin:\nmov ax, data\nmov ds, ax\n"+self.statements_list(token["statements_list"])+"mov ax, 4c00h\nint 21h\n"

    def statements_list(self,token):
        if not token:
            return "nop\n"
        else:
            return self.statement(token["statement"])+(self.statements_list(token.children[1]) if len(token.children)>1 else "")

    def statement(self,token):
        self.for_counter += 1
        label = self.for_counter-1
        if token["variable_identifier"].children[0].value not in self.table:
                raise Exception("Forbidden identifier")
        return self.expression(token["expression"])+ "mov " + token["variable_identifier"].children[0].value + ", ax\n" + \
        self.expression(token["loop_declaration"].children[2])+"mov cx, ax\nsub cx, "+ token["variable_identifier"].children[0].value\
        +"\n jle $endloop" + str(label) + "\n$l" + str(label) + ":\npush cx\n" + self.statements_list(token["statements_list"])+\
        "pop cx\nloop $l"+str(label)+"\n$endloop:"+ str(label)+"\n"


    def expression(self,token):
        if token["multiplier"].children[0].value!="unsigned_integer":
            if token["multiplier"].children[0].children[0].value not in self.table:
                raise Exception("Forbidden identifier")
        return "mov ax, "+token["multiplier"].children[0].children[0].value+"\n"+self.multiplier_list(token.find_in_children("multipliers_list"))

    def multiplier_list(self,token):
        if not token:
            return ""
        else:
            if token["multiplier"].children[0].children[0].value not in self.table:
                raise Exception("This is no such identifier")
            return ("mul "+token["multiplier"].children[0].children[0].value+"\n" if token["multiplication_instruction"].children[0].value == "*"\
            else ("mov dx,0\ndiv " + token["multiplier"].children[0].children[0].value +"\n" if token["multiplication_instruction"].children[0].value == "/"
                  else "mov dx,0\ndiv " + token["multiplier"].children[0].children[0].value +"\nmov ax,dx\n"))+self.multiplier_list(token.find_in_children("multipliers_list"))

class SemanException(Exception):
    def __init__(self, *args, **kwargs):
        super(SemanException, self).__init__(*args, **kwargs)