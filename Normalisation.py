from string import whitespace
import streamlit as st
import re
from time import sleep
import sys
import numpy as np
from tkinter import VERTICAL
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

with open("styles.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

heading = "<div class='title'>Check Normal Form</heading1>"
st.markdown(heading, unsafe_allow_html=True)

try:
    
    attributes = st.text_input("Enter the Attributes :")
    f_d = st.text_input("Enter the Functional Dependencies :")
    #attributes = "A,B,C,D,E,F,G,H"
    attributes = "A,C,D,E,I,G,M,N,R"
    #attributes = "D,A,E,N,R,C,M,F,G"
    relation = attributes.split(",")
    relation.sort()
    print(relation)

    l = set()
    m = set()
    r = set()
    fds = []
    f1 = []
    # n=input("Enter functional Dependency:")
    #f_d = "D->AB,B->A,C->A,F->G,H->FGD,E->A"
    f_d = "D->A,A->E,N->R,R->N,C->M,C->I,RC->G"
    li = f_d.split(",")

    for i in li:
        li1 = i.split("->")
        fds.append(li1)
        f1.append(li1)

    for fd in fds:
        for i in range(2):
            ls = []
            for j in fd[i]:
                ls.append(j)
            fd[i] = ls

    # print(fd)
except ValueError:
    st.error("You have Entered Invalid Page reference string!..")
# 

def closure(R, FD, S):
    '''
    find the closer
    '''
    if not (is_subset(S, R)):
        return []
    result = list(S)
    changed = True
    while(changed):
        changed = False
        for fd in FD:
            LHS = fd[0]
            RHS = fd[1]
            if (is_subset(LHS, result)):
                for att in RHS:
                    if (att not in result):
                        result.append(att)
                        changed = True
    return sorted(result)
# 

def is_subset(X, Y):
    '''
    Check if the list is subset of another list
    '''
    return set(X).issubset(set(Y))
# 

def candidate_keys(R, FD):
    '''
    find candidate keys
    '''
    result = []
    ck = []
    for att_set in subsets(R):
        att_closure = closure(R, FD, att_set)
        if (att_closure == R):
            #check if super key
            iis = False
            for key in ck:
                if is_subset(key, att_set):
                    iis = True
            if iis:
                continue
            ck.append(att_set)
    ls_ck = []
    for i in ck:
        s = ""
        for j in i:
            s += j
        ls_ck.append(s)
    return ls_ck
# 

def subsets(R):
    '''
    Calculate all possible subsets of given list
    Return them in a sorted way (first alphabetic and then length)
    '''
    x = len(R)
    masks = [1 << i for i in range(x)]
    result = []
    for i in range(1, 1 << x):
        r = []
        for mask, ss in zip(masks, R):
            if i & mask:
                r.append(ss)
        result.append(r)
    result.sort()
    result.sort(key=len)
    return result
# 

def prime(ck):
    '''
        takes set of attributes of candidate key and returns set of prime attributes
    '''
    pr = set()
    for i in ck:
        for j in i:
            pr.add(j)
    return pr
# 

def non_prime(pr, R):
    '''
        takes prime attributes and R and returns set of non-prime attributes
    '''
    return R.difference(pr)
# 

def check(string, sub_str):
    if (string.find(sub_str) == -1):
        return 0
    else:
        return 1
# 

def in_np(s, np):
    for i in s:
        if i in np:
            return 1
    return 0

bcnf_v = []; tnf_v = []; twonf_v=[]; b_v = []; t_v = []; t_v_n = []; two_v = []
# 

def check_bcnf(ck, fd):
    ls_left = []
    ls_right = []
    flag = 0
    for fd in fds:
        sl = ""
        for i in fd[0]:
            sl += i
        ls_left.append(sl)

        sr = ""
        for i in fd[1]:
            sr += i
        ls_right.append(sr)
    
    for i in ls_left:
        for j in ck:
            if (check(i, j) == 0): # check substring of ck
                # st.write("Violating BCNF Condition at {}->{}".format(i, ls_right[ls_left.index(i)]))
                b_v.append(i)
                s= i +"->"+ls_right[ls_left.index(i)]
                bcnf_v.append(s)
                flag = 1
                break
    if flag == 1:
        return False
    else:
        return True
# 

def check_3nf(ck, fd, R):
    ls_left = []
    ls_right = []
    flag = 0

    pr = prime(ck)
    np = non_prime(pr, set(R))

    for fd in fds:
        sl = ""
        for i in fd[0]:
            sl += i
        ls_left.append(sl)

        sr = ""
        for i in fd[1]:
            sr += i
        ls_right.append(sr)

    for i in range(len(ls_left)):
        for j in ck:
            if check(ls_left[i], j) == 0 and in_np(ls_right[i], np) == 1:
                t_v.append(ls_left[i])

            if in_np(ls_right[i], np) == 1:
                t_v_n.append(ls_right[i])

            if check(ls_left[i],j) == 0 and in_np(ls_right[i], np) == 1: # check sk and np att
                # st.write("Violating 3NF Condition at {}->{}".format(i, ls_right[ls_left.index(i)]))
                s= ls_left[i] +"->"+ls_right[i]
                tnf_v.append(s)
                flag = 1
                break
    if flag == 1:
        return False
    else:
        return True
# 

def check_2nf(ck, fd, R):
    ls_left = []
    ls_right = []
    flag = 0

    pr = prime(ck)
    np = non_prime(pr, set(R))
    for fd in fds:
        sl = ""
        for i in fd[0]:
            sl += i
        ls_left.append(sl)

        sr = ""
        for i in fd[1]:
            sr += i
        ls_right.append(sr)

    for i in range(len(ls_left)):
        for j in ls_left[i]:
            if j in pr and ls_right[i] in np: # check partial dep.
                # st.write("Violating 2NF Condition at {}->{}".format(i, ls_right[ls_left.index(i)]))
                s= ls_left[i] +"->"+ls_right[i]
                two_v.append(ls_left[i])
                twonf_v.append(s)
                flag = 1
    if flag == 1:
        return False
    else:
        return True

# **********************************

col1,col3, col2 = st.columns([3, 3, 9])
with col1:
    choice = option_menu("", ["Candidate Keys", "Prime Attributes",
                         "Non-Prime Attributes", "Check BCNF", "Check 3NF", "Check 2NF"], orientation=VERTICAL)
    
    ck = candidate_keys(relation, fds)
    pr = prime(ck)
    np = non_prime(pr, set(relation))

    if choice == "Candidate Keys":
        with col3:
            st.write("Rule:")
            st.write("A candidate key is a subset of a super key set where the key which contains no redundant attribute is none other than a Candidate Key.")

        with col2:
            st.write("Candidate keys are :")
            s = set(ck)
            st.write(s)

    elif choice == "Prime Attributes":
        with col3:
            st.write("Rule:")
            st.write("An attribute that is a part of one of the candidate keys is known as prime attribute.")
        with col2:
            st.write("Prime Attributes are :")

            st.write(pr)

    elif choice == "Non-Prime Attributes":
        with col3:
            st.write("Rule:")
            st.write("Attributes of the relation which does not exist in any of the possible candidate keys of the relation, such attributes are called non prime attributes.")
        with col2:
            # np = non_prime(pr, set(relation))
            st.write("Non-Prime Attributes are :")
            st.write(np)
    
    elif choice == "Check BCNF":
        with col3:
            st.write("Rule:")
            st.write(" A table is in BCNF if every functional dependency X->Y, X is the super key of the table.")
        with col2:
            with st.container():
                st.write("Check BCNF :")
                if check_bcnf(ck, fds) == True and len(ck)!=0:
                    st.write("Relation is in BCNF")
                else:
                    st.write("Violating BCNF Condition at : ")
                    s = set(bcnf_v)
                    st.write(s)
            with st.container():
                sk = set(b_v)
                st.write(f"{sk} \t are not the Super keys")      

    elif choice == "Check 3NF":
        with col3:
            st.write("Rule:")
            st.write("Relation must be in 2NF, in every FD X -> Y, X is super key OR Y is prime attribute.")
        with col2:
            with st.container():
                st.write("Check 3NF :")
                if check_3nf(ck, fds, relation) == True and len(ck)!=0:
                    st.write("Relation is in 3NF")
                else:
                    st.write("Violating 3NF Condition at : ")
                    s = set(tnf_v)
                    st.write(s)  
            
            with st.container():
                sk = set(t_v)
                st.write(f"{sk} \t are not the Super keys")

                sk = set(t_v_n)
                st.write(f"{sk} \t are not prime attributes")

    elif choice == "Check 2NF":
        with col3:
            st.write("Rule:")
            st.write("a relation is in 2NF if it is in 1NF and every non-prime attribute of the relation is dependent on the whole of every candidate key.")
        with col2:
            with st.container():
                st.write("Check 2NF :")
                if check_2nf(ck, fds, relation) == True and len(ck)!=0:
                    st.write("Relation is in 2NF")
                else:
                    st.write("Violating 2NF Condition at : ")
                    s = set(twonf_v)
                    st.write(s) 
            
            with st.container():
                sk = set(two_v)
                st.write(f"{sk} \t are prime attribute") 
    else:
        with col2:
            print("Relation is in 1NF")