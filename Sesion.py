import streamlit as st
st.set_page_config(layout='wide')
pg = st.navigation([st.Page("Bonificaciones.py"), st.Page("Descuentos.py")])
pg.run()
st.sidebar.link_button('Repositorio GitHub','https://github.com/FACS2000/moduloETE.git')

