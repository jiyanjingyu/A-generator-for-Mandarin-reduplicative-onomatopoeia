#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prettytable import PrettyTable

class Tree:
    def __init__(self,
                 data):
        self.data = data
        self.children = []
                 
    def add_subtree(self, subtree):
        self.children.append(subtree)

    def size(self):
        if self.children == []:
            return 1
        return 1 + sum(list(map(lambda x:x.size(),self.children)))
    
    def yld(self):
        if self.children == []:
            return str(self.data)
        else:
            string = ""
            yld_seq = list(map(lambda x:x.yld(),self.children))
            for pos in range(len(self.children)):
                string = string + yld_seq[pos]
            return string

    def depth(self):
        if self.children == []:
            return 0
        else:
            depth_seq = list(map(lambda x:x.depth(),self.children))
            return 1 + max(depth_seq)
                      
    def is_valid_VL_tree(self):
        '''the function takes a tree and returns True if it is a valid variably leafed tree'''
        if self.children == []:
            return isinstance(self.data,str) or isinstance(self.data,int)
        else:
            if isinstance(self.data,int):
                return False
            else:
                values = list(map(lambda x:x.is_valid_VL_tree(),self.children))
        if False in values:
            return False
        else:
            return True
        
    def is_valid_normal_tree(self):
        '''the function takes a tree and returns True if it is a valid normal tree'''
        if isinstance(self.data,int):
            return False
        else:
            values = list(map(lambda x:x.is_valid_VL_tree(),self.children))
        if False in values:
            return False
        else:
            return True

    def substitute(self,treelist):
        if (self.children == []) and (isinstance(self.data, str)):
            return self
        elif (self.children == []) and (isinstance(self.data, int)):
            variable = self.data
            return treelist[variable-1]
        else:
            newkids = list(map(lambda x:x.substitute(treelist),self.children))
            t = Tree(self.data)
            t.children = newkids
            return t
        
    def find_variable(self):
        if self.children == [] and isinstance(self.data, int):
            return [self.data]
        else:
            variables = []
            v_seq = list(map(lambda x:x.find_variable(),self.children))
            for i in v_seq:
                variables = variables + i
            return variables
        
    def show(self):
        str_data = str(self.data)
        if self.children == []:
            return str_data
        else:
            str_children = list(map(lambda x:x.show(),self.children))
            return str_data + '[ ' + ' '.join(str_children) + ']'  

# top-down tree transducer with input and output alphabet                       
class DTDTT():
    def __init__(self,
                 states,
                 input_alphabet,
                 output_alphabet,
                 q0,
                 transitions):
        self.input_alphabet = input_alphabet
        self.transitions = transitions
        self._delta_dict = self._delta_dict()
        self._omega_dict = self._omega_dict()
        self.q0 = q0
        
    def _delta_dict(self):

        d = dict()    
        for (q,a,n,qstring,t) in self.transitions:
            if a in self.input_alphabet:
                d[(q,a,n)] = qstring
        return d
    
    def _omega_dict(self):
        d = dict()
        
        for (q,a,n,qstring,t) in self.transitions:
            if a in self.input_alphabet:
                d[(q,a,n)] = t
        return d    
        
    def process(self,q,tree):
        if tree.children == []:
            return self._omega_dict[(q,tree.data,0)]
        
        else:
            qlist = self._delta_dict[(q,tree.data,len(tree.children))]

            newtree = self._omega_dict[(q,tree.data,len(tree.children))].substitute(list(map(lambda x,y :self.process(x,y),qlist,tree.children)))
            return newtree
    # return empty string if the transformation is undefined     
    def transforms(self,tree):
        try:
            t = self.process(self.q0,tree)
            return t
        except:
            return ''

# bottom-up tree transducer
class DBUTT():
    def __init__(self,
                 states,
                 input_alphabet,
                 output_alphabet,
                 final,
                 transitions):
        self.input_alphabet = input_alphabet
        self.transitions = transitions
        self._delta_dict = self._delta_dict()
        self._omega_dict = self._omega_dict()
        self.final = final

    def _delta_dict(self):

        d = dict()   
        for (qstring,a,q,t) in self.transitions:
            if a in self.input_alphabet:
                d[(tuple(qstring),a)] = q
        return d

    def _omega_dict(self):
        d = dict()

        for (qstring,a,q,t) in self.transitions:
            if a in self.input_alphabet:
                d[(tuple(qstring),a)] = t
        return d

    def process(self,tree):
        if tree.children == []:
            return (self._delta_dict[((),tree.data)],self._omega_dict[((),tree.data)])
        else:
            qt_pair_list = list(map(lambda x:self.process(x),tree.children))
            qlist = [x for (x,y) in qt_pair_list]
            treelist = [y for (x,y) in qt_pair_list]
            qtuple = tuple(qlist)
            q = self._delta_dict[(qtuple,tree.data)]
            vlt = self._omega_dict[(qtuple,tree.data)]
            t = vlt.substitute(treelist)
            return (q,t)
    # return empty string if the transformation is undefined
    def transforms(self,tree):
        try:
            q,t = self.process(tree)
            if q in self.final:
                return t
            else:
                return ''
        except:
            return ''

# variable-leafed trees for substitution
a = Tree('a')
i = Tree('i')
ua = Tree('ua')
e = Tree('ə')
u = Tree('u')
i_1 = Tree('ɿ')
d = Tree('t')
t = Tree('tʰ')
b = Tree('p')
p = Tree('pʰ')
l = Tree('l')
g = Tree('k')
k = Tree('kʰ')
h = Tree('x')
j = Tree('tɕ')
q = Tree('tɕʰ')
x = Tree('ɕ')
z = Tree('ts')
c = Tree('tsʰ')
s = Tree('s')
zh = Tree('tʂ')
ch = Tree('tʂʰ')
sh = Tree('ʂ')
ng = Tree('ŋ')

one = Tree(1)
two = Tree(2)
three = Tree(3)
four = Tree(4)

t1 = Tree('W')
t1.add_subtree(one)
t1.add_subtree(two)
t1.add_subtree(one)
t1.add_subtree(two)

t2 = Tree('S')
t2.add_subtree(one)
t2.add_subtree(two)

t2_2 = Tree('W')
t2_2.add_subtree(one)
t2_2.add_subtree(two)

t3 = Tree('S')
t3.add_subtree(one)
t3.add_subtree(two)
t3.add_subtree(three)

t4 = Tree('W')
t4.add_subtree(one)
t4.add_subtree(two)
t4.add_subtree(three)
t4.add_subtree(four)

t5 = Tree('W')
t5.add_subtree(one)
t5.add_subtree(one)
t5.add_subtree(two)
t5.add_subtree(two)

t6 = Tree('W')
t6.add_subtree(one)
t6.add_subtree(one)

t7 = Tree('W')
t7.add_subtree(one)
t7.add_subtree(one)
t7.add_subtree(two)

t8 = Tree('W')
t8.add_subtree(one)
t8.add_subtree(two)
t8.add_subtree(two)

t9 = Tree('S')
t9.add_subtree(one)
t9.add_subtree(i_1)

# alphabet
consonant = ['p','pʰ','t','tʰ','m','n','ŋ','tɕ','tɕʰ','ɕ','ts','tsʰ','s','k','kʰ','tʂ','tʂʰ','ʂ','x','l']

vowel = ['a','i','u','uo','iɛ','ua','ə','au','ou','ia','iou','uei','uai','y','iau','ei','ai','uə','ɤ','ɿ']

treelist = [a,i,ua,e,u,i_1,k,h,d,t,b,p,l,g,k,j,q,x,z,c,s,zh,ch,sh,ng]

# find the corresponding tree in the treelist given a symbol in the alphabet
def find_tree(x):
    for i in treelist:
        if i.data == x:
            return i

# prepositional reduplication    
dtdtt1 = DTDTT(states = ['q','qf'],
               input_alphabet = consonant+vowel+['S','W'],
               output_alphabet = consonant+vowel+['S'+'W'],
               q0 = 'qf',
               # represent transitions with for loop
               transitions = [('q',c,0,[],find_tree(c)) for c in consonant]+
               [('q',v,0,[],find_tree(v)) for v in vowel]+
               [('q','S',2,['q','q'],t2),
                ('qf','W',2,['q','q'],t1),
                ('q','S',3,['q','q','q'],t3),
                ('qf','W',1,['q'],t6)])
    
dtdtt2 = DTDTT(states = ['q','qf','qi'],
               input_alphabet = set(consonant+vowel+['S','W'])-{'i','y','ɿ'},
               output_alphabet = consonant+vowel+['S','W'],
               q0 = 'qf',
               # make change to the node with 'qi' state
               transitions = [('q',c,0,[],find_tree(c)) for c in consonant]+
               [('qi',c,0,[],find_tree(c)) for c in set(consonant)-{'k','kʰ','x','tʂ','tʂʰ','ʂ'}]+
               [('qi','k',0,[],j),
                ('qi','kʰ',0,[],q),
                ('qi','x',0,[],x),
                ('qi','tʂ',0,[],z),
                ('qi','tʂʰ',0,[],c),
                ('qi','ʂ',0,[],s)]+             
               [('q',v,0,[],find_tree(v)) for v in vowel]+
               [('qi',v,0,[],i) for v in vowel]+               
               [('qi','S',2,['qi','qi'],t2),
                ('qf','W',4,['qi','qi','q','q'],t4),
                ('q','S',2,['q','q'],t2),
                ('qi','S',3,['qi','qi','q'],t3),
                ('q','S',3,['q','q','q'],t3),
                ('qf','W',2,['qi','q'],t2_2)])

dbutt2 = DBUTT(states = ['q','qf','qz','qi'],
               input_alphabet = consonant+vowel+['S','W'],
               output_alphabet = consonant+vowel+['S','W'],
               final = ['qf'],
               # change [i] to [ɿ] in the reduplicant when followed by [ts], [tsʰ], [s]
               transitions = [([],c,'q',find_tree(c)) for c in set(consonant)-{'ts','tsʰ','s'}]+
               [([],c,'qz',find_tree(c)) for c in {'ts','tsʰ','s'}]+           
               [([],v,'q',find_tree(v)) for v in set(vowel)-{'i'}]+            
               [([],'i','qi',i),
                (['q','q'],'S','q',t2),
                (['q','qi'],'S','q',t2),                
                (['qz','q'],'S','q',t2),
                (['qz','qi'],'S','qz',t9),
                (['q','q','q'],'S','q',t3),
                (['q','qi','q'],'S','q',t3),
                (['qz','q','q'],'S','q',t3),
                (['qz','qi','q'],'S','qz',t3),                
                (['q','qz','q','q'],'W','qf',t4),
                (['qz','q','q','q'],'W','qf',t4),
                (['qz','qz','q','q'],'W','qf',t4),
                (['q','q','q','q'],'W','qf',t4),
                (['q','q'],'W','qf',t2_2),
                (['qz','q'],'W','qf',t2_2)])

# postpositional reduplication   
dtdtt3 = DTDTT(states = ['q','qf'],
               input_alphabet = consonant+vowel+['S','W'],
               output_alphabet = consonant+vowel+['S','W'],
               q0 = 'qf',
               transitions = [('q',c,0,[],find_tree(c)) for c in consonant]+
               [('q',v,0,[],find_tree(v)) for v in vowel]+
               [('q','S',2,['q','q'],t2),
                ('qf','W',2,['q','q'],t5),
                ('q','S',3,['q','q','q'],t3),
                ('qf','W',1,['q'],t6)])
    
dtdtt4 = DTDTT(states = ['q','qf','ql'],
               input_alphabet = set(consonant+vowel+['S','W'])-{'l'},
               output_alphabet = consonant+vowel+['S','W'],
               q0 = 'qf',
               # make change to the node with 'ql' state
               transitions = [('q',c,0,[],find_tree(c)) for c in consonant]+
               [('q',v,0,[],find_tree(v)) for v in vowel]+
               [('ql',v,0,[],find_tree(v)) for v in set(vowel)-{'ua','ɿ'}]+
               [('ql','ua',0,[],a),('ql','ɿ',0,[],i)]+
               [('ql',c,0,[],l) for c in consonant]+               
               [('ql','S',2,['ql','ql'],t2),
                ('qf','W',4,['q','ql','q','ql'],t4),
                ('q','S',2,['q','q'],t2),
                ('ql','S',3,['ql','ql','q'],t3),
                ('q','S',3,['q','q','q'],t3),
                ('qf','W',2,['q','ql'],t2_2)])

# partial reduplication
dtdtt5 = DTDTT(states = ['q','qf'],
               input_alphabet = consonant+vowel+['S','W'],
               output_alphabet = consonant+vowel+['S','W'],
               q0 = 'qf',
               transitions = [('q',c,0,[],find_tree(c)) for c in consonant]+
               [('q',v,0,[],find_tree(v)) for v in vowel]+
               [('q','S',2,['q','q'],t2),
                ('qf','W',2,['q','q'],t7),
                ('q','S',3,['q','q','q'],t3)])

dtdtt6 = DTDTT(states = ['q','qf'],
               input_alphabet = consonant+vowel+['S','W'],
               output_alphabet = consonant+vowel+['S','W'],
               q0 = 'qf',
               transitions = [('q',c,0,[],find_tree(c)) for c in consonant]+
               [('q',v,0,[],find_tree(v)) for v in vowel]+
               [('q','S',2,['q','q'],t2),
                ('qf','W',2,['q','q'],t8),
                ('q','S',3,['q','q','q'],t3)])

# process ABAC pattern
dtdtt7 = DTDTT(states = ['q','qf','ql','qi'],
               input_alphabet = set(consonant+vowel+['S','W'])-{'l','i'},
               output_alphabet = consonant+vowel+['S','W'],
               q0 = 'qf',
               transitions = [('q',c,0,[],find_tree(c)) for c in consonant]+
               [('q',v,0,[],find_tree(v)) for v in vowel]+
               [('ql',v,0,[],find_tree(v)) for v in set(vowel)-{'ua'}]+
               [('ql','ua',0,[],a)]+
               [('ql',c,0,[],l) for c in consonant]+
               [('qi',c,0,[],l) for c in consonant]+
               [('qi',v,0,[],i) for v in vowel]+                 
               [('ql','S',2,['ql','ql'],t2),
                ('qf','W',4,['q','qi','q','ql'],t4),
                ('q','S',2,['q','q'],t2),
                ('qi','S',2,['ql','qi'],t2),
                ('ql','S',3,['ql','ql','q'],t3),
                ('qi','S',3,['ql','qi','q'],t3),
                ('q','S',3,['q','q','q'],t3)])

# define a function for each pattern
def AA(tree):
    t = dtdtt1.transforms(tree)
    if t:
        return t.show()
    else:
        return ''

def AAA(tree):
    t = dtdtt6.transforms(dtdtt1.transforms(tree))
    if t:
        return t.show()
    else:
        return ''

def AAAA(tree):
    t = dtdtt1.transforms(dtdtt1.transforms(tree))
    if t:
        return t.show()
    else:
        return ''

def AB(tree):
    t = dtdtt4.transforms(dtdtt3.transforms(tree))
    if t:
        return t.show()
    else:
        return '' 

def BA(tree):
    t = dbutt2.transforms(dtdtt2.transforms(dtdtt1.transforms(tree)))
    if t:
        return t.show()
    else:
        return '' 

def ABB(tree):
    t = dtdtt6.transforms(dtdtt4.transforms(dtdtt3.transforms(tree)))
    if t:
        return t.show()
    else:
        return '' 
    
def BBA(tree):
    t = dtdtt5.transforms(dbutt2.transforms(dtdtt2.transforms(dtdtt1.transforms(tree))))
    if t:
        return t.show()
    else:
        return ''

def ABAB(tree):
    t = dtdtt1.transforms(dtdtt4.transforms(dtdtt3.transforms(tree)))
    if t:
        return t.show()
    else:
        return ''

def BABA(tree):
    t = dtdtt1.transforms(dbutt2.transforms(dtdtt2.transforms(dtdtt1.transforms(tree))))
    if t:
        return t.show()
    else:
        return ''

def AABB(tree):
    t = dtdtt3.transforms(dtdtt4.transforms(dtdtt3.transforms(tree)))
    if t:
        return t.show()
    else:
        return ''  

def BBAA(tree):
    t = dtdtt3.transforms(dbutt2.transforms(dtdtt2.transforms(dtdtt1.transforms(tree))))
    if t:
        return t.show()
    else:
        return ''

def CDAB(tree):
    t = dbutt2.transforms(dtdtt2.transforms(dtdtt1.transforms(dtdtt4.transforms(dtdtt3.transforms(tree)))))
    if t:
        return t.show()
    else:
        return ''

def BDAC(tree):
    t = dtdtt4.transforms(dtdtt3.transforms(dbutt2.transforms(dtdtt2.transforms(dtdtt1.transforms(tree)))))
    if t:
        return t.show()
    else:
        return ''

def ABAC(tree):
    t = dtdtt7.transforms(dtdtt3.transforms(dtdtt1.transforms(tree)))
    if t:
        return t.show()
    else:
        return ''

# testing with monosyllabic onomatopoeia as input  
ba_1 = Tree('S')
ba_1.add_subtree(b)
ba_1.add_subtree(a)

ba = Tree('W')
ba.add_subtree(ba_1)

di_1 = Tree('S')
di_1.add_subtree(d)
di_1.add_subtree(i)

di = Tree('W')
di.add_subtree(di_1)

da_1 = Tree('S')
da_1.add_subtree(d)
da_1.add_subtree(a)

da = Tree('W')
da.add_subtree(da_1)

ta_1 = Tree('S')
ta_1.add_subtree(t)
ta_1.add_subtree(a)

ta = Tree('W')
ta.add_subtree(ta_1)

pa_1 = Tree('S')
pa_1.add_subtree(p)
pa_1.add_subtree(a)

pa = Tree('W')
pa.add_subtree(pa_1)

ding_1 = Tree('S')
ding_1.add_subtree(d)
ding_1.add_subtree(i)
ding_1.add_subtree(ng)

ding = Tree('W')
ding.add_subtree(ding_1)

deng_1 = Tree('S')
deng_1.add_subtree(d)
deng_1.add_subtree(e)
deng_1.add_subtree(ng)

deng = Tree('W')
deng.add_subtree(deng_1)

dong_1 = Tree('S')
dong_1.add_subtree(d)
dong_1.add_subtree(u)
dong_1.add_subtree(ng)

dong = Tree('W')
dong.add_subtree(dong_1)

dang_1 = Tree('S')
dang_1.add_subtree(d)
dang_1.add_subtree(a)
dang_1.add_subtree(ng)

dang = Tree('W')
dang.add_subtree(dang_1)

du_1 = Tree('S')
du_1.add_subtree(d)
du_1.add_subtree(u)

du = Tree('W')
du.add_subtree(du_1)

gua_1 = Tree('S')
gua_1.add_subtree(g)
gua_1.add_subtree(ua)

gua = Tree('W')
gua.add_subtree(gua_1)

hua_1 = Tree('S')
hua_1.add_subtree(h)
hua_1.add_subtree(ua)

hua = Tree('W')
hua.add_subtree(hua_1)

ga_1 = Tree('S')
ga_1.add_subtree(g)
ga_1.add_subtree(a)

ga = Tree('W')
ga.add_subtree(ga_1)

zha_1 = Tree('S')
zha_1.add_subtree(zh)
zha_1.add_subtree(a)

zha = Tree('W')
zha.add_subtree(zha_1)

sha_1 = Tree('S')
sha_1.add_subtree(sh)
sha_1.add_subtree(a)

sha = Tree('W')
sha.add_subtree(sha_1)

gu_1 = Tree('S')
gu_1.add_subtree(g)
gu_1.add_subtree(u)

gu = Tree('W')
gu.add_subtree(gu_1)

guang_1 = Tree('S')
guang_1.add_subtree(g)
guang_1.add_subtree(ua)
guang_1.add_subtree(ng)

guang = Tree('W')
guang.add_subtree(guang_1)

pang_1 = Tree('S')
pang_1.add_subtree(p)
pang_1.add_subtree(a)
pang_1.add_subtree(ng)

pang = Tree('W')
pang.add_subtree(pang_1)

hong_1 = Tree('S')
hong_1.add_subtree(h)
hong_1.add_subtree(u)
hong_1.add_subtree(ng)

hong = Tree('W')
hong.add_subtree(hong_1)

kuang_1 = Tree('S')
kuang_1.add_subtree(k)
kuang_1.add_subtree(ua)
kuang_1.add_subtree(ng)

kuang = Tree('W')
kuang.add_subtree(kuang_1)

A = [ba,di,da,ta,ding,deng,dong,dang,du,gua,ga,gu,guang,pang,hong,kuang,pa,sha,hua,zha]

# testing with disyllabic onomatopoeia as input
ji = Tree('S')
ji.add_subtree(j)
ji.add_subtree(i)

baji = Tree('W')
baji.add_subtree(ba_1)
baji.add_subtree(ji)

guaji = Tree('W')
guaji.add_subtree(gua_1)
guaji.add_subtree(ji)

ka = Tree('S')
ka.add_subtree(k)
ka.add_subtree(a)

cha = Tree('S')
cha.add_subtree(ch)
cha.add_subtree(a)

kacha = Tree('W')
kacha.add_subtree(ka)
kacha.add_subtree(cha)

bada = Tree('W')
bada.add_subtree(ba_1)
bada.add_subtree(da_1)

gudong = Tree('W')
gudong.add_subtree(gu_1)
gudong.add_subtree(dong_1)

ci = Tree('S')
ci.add_subtree(c)
ci.add_subtree(i_1)

la = Tree('S')
la.add_subtree(l)
la.add_subtree(a)

cila = Tree('W')
cila.add_subtree(ci)
cila.add_subtree(la)

# words with temporary meaning cannot go through AABB pattern
AB_temp = [baji,guaji,kacha,bada,gudong]

# words with continuous meaning can go through AABB pattern
AB_cont = [cila]

# use for loop to print out all the testing word in the same format
for i in A:
    t = PrettyTable()
    t.field_names = ["Input","Pattern", "Output"]
    
    t.add_row([i.show(),'AA',AA(i)])
    t.add_row([i.show(),'AAA',AAA(i)])
    t.add_row([i.show(),'AAAA',AAAA(i)])
    t.add_row([i.show(),'AB',AB(i)])
    t.add_row([i.show(),'BA',BA(i)])
    t.add_row([i.show(),'ABB',ABB(i)])
    t.add_row([i.show(),'BBA',BBA(i)])
    t.add_row([i.show(),'ABAB',ABAB(i)])
    t.add_row([i.show(),'BABA',BABA(i)])
    t.add_row([i.show(),'AABB',AABB(i)])
    t.add_row([i.show(),'BBAA',BBAA(i)])
    t.add_row([i.show(),'CDAB',CDAB(i)])
    t.add_row([i.show(),'BDAC',BDAC(i)])
    t.add_row([i.show(),'ABAC',ABAC(i)])

    print(t) 
    
def rhyming(tree):
    if len(tree.children[0].children)==len(tree.children[1].children)==2:
        if tree.children[0].children[1]==tree.children[1].children[1]:
            return True
    elif len(tree.children[0].children)==len(tree.children[1].children)==3:
        if tree.children[0].children[1]==tree.children[1].children[1] and tree.children[0].children[2]==tree.children[1].children[2]:
            return True
    else:
        return False
            
for i in AB_cont:
    t = PrettyTable()
    t.field_names = ["Input","Pattern", "Output"]
    
    t.add_row([i.show(),'ABAB',AA(i)])
    if rhyming(i):
        t.add_row([i.show(),'CDAB',BA(i)])
    else:
        t.add_row([i.show(),'CDAB',''])
    t.add_row([i.show(),'AABB',dtdtt3.transforms(i).show()])
    
    print(t)    
    
for i in AB_temp:
    t = PrettyTable()
    t.field_names = ["Input","Pattern", "Output"]
    
    t.add_row([i.show(),'ABAB',AA(i)])
    if rhyming(i):
        t.add_row([i.show(),'CDAB',BA(i)])
    else:
        t.add_row([i.show(),'CDAB',''])
    
    print(t) 
