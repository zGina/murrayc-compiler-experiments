class LR_item(object):  
    def __init__(self,id):
        self.goto = []  #char
        self.gotoitem = []  #int
        self.productions = []  
        self.id = id
        
def get_closure(char, LR0_item, CFG):
    #若是终端字符
    if not char.isupper():
        return
    else:
    #非终端字符
        for i in range(0, len(CFG[char])):
            rh = "." + CFG[char][i]
            new=[char, rh]
            if new not in LR0_item.productions:
                LR0_item.productions.append(new)

#全局变量GOTO {string,int}  产生式->项目/状态集编号
#p135 action 和 goto 不会冲突，在实际应用中直接将他们重叠，用同一数组元素表示 
GOTO = dict()
def swap(c, i, j):
    c = list(c)
    c[i], c[j] = c[j], c[i]
    return ''.join(c)


#构造识别活前缀的 DFA ，即项目集
def get_LR0_items(LR0_items, CFG,itemid):
    print("\nI" + str(itemid) )
    cur_item=LR0_items[itemid]
    #先对当前项目集求闭包
    i=0
    while(i<len(cur_item.productions)):
        rh =cur_item.productions[i][1]
        #find B in A->/alpha .B /belta
        index=rh.index('.')
        if (index == len(rh) - 1):
            i+=1
            continue
        lookahead=rh[index+1]
        get_closure(lookahead, cur_item, CFG)
        i+=1
    #迭代项目集中的每一个产生式
    #分为四种情况：①规约②移进③待约④结束
    
    for i in range(0, len(cur_item.productions)):
        lh = cur_item.productions[i][0]
        rh = cur_item.productions[i][1]
        production=lh+"->"+rh
        #若 . 已在末尾，即规约
        index=rh.index('.')
        if (index == len(rh) - 1):
            print(production)
            continue
        lookahead=rh[index+1]
        new_itemid = len(LR0_items)
        #对每一个有可能的符号转移，生成一个新的对应的状态集
        #不需要遍历符号表，减小开销
        if lookahead not in cur_item.goto:
            if production not in GOTO:               
                new_lr_item = LR_item(new_itemid)
                pos = rh.index('.')
                #移进！
                rh=swap(rh,pos,pos+1)
                new_lr_item.productions.append([lh, rh])
                cur_item.goto.append(lookahead)
                cur_item.gotoitem.append(new_itemid)
                GOTO[production] = new_itemid
                LR0_items.append(new_lr_item)
            else:
                #全局GOTO表中已经存在
                cur_item.goto.append(lookahead)
                cur_item.gotoitem.append(GOTO[production])
            print(production+"\t\tgoto("+lookahead+")="+"I"+str(GOTO[production]))
        else:
            #当前item某个符号对应的new_item已经生成
            #移进,加入该new_item
            pos = rh.index('.')
            rh = swap(rh, pos, pos + 1)

            index=cur_item.goto.index(lookahead)
            goto_itemid=cur_item.gotoitem[index]
            goto_item=LR0_items[goto_itemid]
            if [lh, rh] not in goto_item.productions:
                goto_item.productions.append([lh,rh])
            rh = swap(rh, pos, pos + 1)
            print(lh+"->"+rh)

def get_LR_table(LR0_items):
    LR_table = []
    Item0=[]
    for item in LR0_items:
        for i in item.goto:
            
            Item0.append({i: item.goto_item})
            


#load CFG while initialing item[0]
def load_CFG(filename):
    LR_items = []
    from collections import defaultdict
    CFG = defaultdict(list)
    with open(filename, 'r') as file:
        line = file.readline().replace('\n', '')
        lr_item = LR_item(0)
        #拓广文法
        start=line
        lr_item.productions.append([line + "'", "."+line])
        line=file.readline().replace('\n', '')
        while (line):     
            line=line.split("->")
            CFG[line[0]].append(line[1])
            if(line[0]==start):
                lr_item.productions.append([line[0], "."+line[1]])
            line = file.readline().replace('\n', '')
    LR_items.append(lr_item)       
    file.close()
    return LR_items,CFG
# E
# E->E+T
# E->T(E)
# T->T*F
# T->F
# T->Fi
# F->(E)
# F->i
def analysis(inputs,GOTO):
    i = 0
    left=len(inputs)
    while (GOTO(i)):
        left -= 1
        
def load_input(filename):
    inputs=[]
    with open(filename, 'r') as file:
        line = file.readline().replace('\n', '')
        while (line):     
            inputs.append(line)
            line = file.readline().replace('\n', '') 
    file.close()
    return inputs
if __name__ == "__main__":
    filename="2019-autumn/compiler/murrayc-compiler-experiments/src/chapter_04/grammar_1.txt"
    testname="2019-autumn/compiler/murrayc-compiler-experiments/src/chapter_04/test_1.txt"
    LR_items, CFG = load_CFG(filename)
    inputs=load_input(testname)
    itemid = 0
    while (itemid < len(LR_items)):
        get_LR0_items(LR_items, CFG, itemid)
        itemid+=1
    State = [0]
    Char = ['#']
    input_string = list(inputs[0])
    input_string.append("#")
    for i in input_string:
        if i == "#":
            print(inputs[0] + " correct！")
            break
        cur_item = LR_items[State[-1]]
        # if cur_item.id == 1:
        #     print(inputs[0]+" correct！")
        #     break
        if cur_item.goto == []:
            handle=cur_item.productions[0][0]
            rh = cur_item.productions[0][1]
            print("规约"+handle+"->"+rh)
            for j in range(0, len(rh)-1):
                Char.pop()
            Char.append(handle)
            State.pop()
            pre_item = LR_items[State[-1]]
            if handle in  pre_item.goto:
                index=pre_item.goto.index(handle)
                new_state=LR_items[State[-1]].gotoitem[index]
                State.append(new_state)
            print("当前状态栈为：")
            print(State)
            print("当前符号栈为：")
            print(Char)

        cur_item = LR_items[State[-1]]   
        if i in cur_item.goto:
            print("移进"+i)
            Char.append(i)
            index=cur_item.goto.index(i)
            State.append(cur_item.gotoitem[index])
        else:
            print("error")
            break
        print("当前状态栈为：")
        print(State)
        print("当前符号栈为：")
        print(Char)
        
            
 
    