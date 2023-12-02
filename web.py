import streamlit as st
st.title('PlayMakerAsm')

name = st.text_input("Name","Sample")
action_wait_time = float(st.text_input('action_wait_time','0.01'))
state_wait_time = float(st.text_input('state_wait_time','0.01'))

import assembler

source = st.text_area(
    "source", 
"""
            INT         I      0    
            INT         END    10    
            INT         STEP   1    

            INT         TMP    0    
            STR         OUT    ""    

;head
HEAD        LDI    TMP           I    
            SUB    TMP           END    
            JPL    TMP           END    
            JZE    TMP           END    

;Main
            FMS    OUT           {0}         I   
            PRT    OUT    

;tail
TAIL        ADD                  I           STEP    
            JMP    HEAD    

;end
END         LDI    TMP           TMP
""",1000)

if st.button("Asm"):
    result = assembler.assemble(name,source,action_wait_time,state_wait_time)
    st.text_area("result",result,100000)
    