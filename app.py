import streamlit as st
import json
import random

def app():
    
    def wipe_all():
        st.session_state.pick = random.randrange(4)
        st.session_state["answer"] = ""
        st.session_state.proceed = False
        st.session_state.pick_from = choices[choice]
        
    def keep_pick_button(pick):
        st.session_state.pick = pick
        st.session_state.proceed = True
        st.session_state.pick_from = choices[choice]
        
    def keep_pick_answer(pick):
        st.session_state.pick = pick
        st.session_state.proceed = True
        
    def new_pick(pick, choice):
        if len(st.session_state.pick_from)>1:
            st.session_state.pick_from.pop(pick)
        else:
            st.session_state.pick_from = choices[choice]
            
        st.session_state.pick = random.randrange(len(st.session_state.pick_from))
        st.session_state["answer"] = ""
        st.session_state.proceed = True
        
    st.title("Deutsch üben!")
    
    st.markdown(""" ### Hier ist eine einfache App, mit der man Deutsch üben kann. Wähl aus, was du üben möchtest und fang an!
    """)

    with open('files/grammatik.json', 'r') as f:
        grammatik = json.load(f)
        
    with open('files/vokabular.json', 'r') as f:
        vokabular = json.load(f)
        
    with open('files/saetze.json', 'r') as f:
        saetze = json.load(f)
        
        
    mix = grammatik+vokabular+saetze
    
    choices = {'Grammatik': grammatik, 
               'Vokabular': vokabular,
               'Ganze Sätze übersetzen': saetze,
               'Mix!': mix
              }
    choice = st.radio('Was möchtest du üben?', ['Grammatik', 
                                                'Vokabular',
                                                'Ganze Sätze übersetzen', 
                                                'Mix!'], on_change=wipe_all)
    
    if "pick_from" not in st.session_state:
        st.session_state.pick_from = choices[choice]
    
    if "pick" not in st.session_state:
        st.session_state.pick = random.randrange(len(st.session_state.pick_from))
        st.session_state.proceed = False
     
    st.button('Start!', on_click=keep_pick_button, args=(st.session_state.pick,))
    if st.session_state.proceed:
        st.write('----------------------------------')
        st.write(st.session_state.pick_from[st.session_state.pick]['q'])

        answer = st.text_input('Deine Antwort (drück "Enter", um die richtige Antwort zu sehen)','', on_change=keep_pick_answer, args=(st.session_state.pick,), key='answer')
        if answer:
            st.write('Die richtige Antwort: ', st.session_state.pick_from[st.session_state.pick]['a'])
            
            if 'help' in st.session_state.pick_from[st.session_state.pick]:
                help_me = st.session_state.pick_from[st.session_state.pick]['help']
                
                if isinstance(help_me, list):
                    for verb in help_me:
                        st.write(modal_verben_dfs[verb])
                else:
                    st.write(modal_verben_dfs[help_me])
                if help_me=='sollen' or (isinstance(help_me, list) and 'sollen' in help_me):
                    st.write('Der Unterschied zwischen Präteritum und Konjuktiv 2 ergibt sich aus dem Kontext. Oder man benutzt eine komplexere Verwendung von "sollen" für Vergangenheit.')

            st.button('Neue Frage!', on_click=new_pick, args=(st.session_state.pick, choice))

    
if __name__ == '__main__':
    app()
