import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from time import sleep

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 1
submittedTable=None
uploaded_rules_file =None
uploaded_combined_rules_file=None
monthSelect=1
monthFile_Desc=None
file_path_d='Formato de Reglas Desc.xlsx'
with open(file_path_d, "rb") as file:
    file_data_d = file.read()


if "uploader_key_desc" not in st.session_state:
    st.session_state.uploader_key_desc = 1

if "file_name_desc" not in st.session_state:
    st.session_state.file_name_desc = 'Formato de Reglas Desc.xlsx'


# File uploader for Excel
uploaded_file = st.sidebar.file_uploader('Suba el archivo de data general', type='xlsx',label_visibility='collapsed')


month_dict = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}

monthSelect = st.sidebar.selectbox(
    'Mes', 
    options=list(month_dict.keys()), 
    format_func=lambda name: name, 
    placeholder="Escoja un Mes",index=None
)
if monthSelect is not None:
    monthFile_Desc = month_dict[monthSelect]

supplierFile= st.sidebar.selectbox('Proveedor',('AND','ETE','4LO','GUR','PPN','VER','QLP','TCM','PFA','ALT','ADA','BDF','QSZ','COL','ALI','NPU','SAL','K&M','SQL','SAN','ZAI',
'ZUR','NES','UNI','PRY','UNS','FIN','MOL','RSA','COR','COP','GLO','JHO','CDP'),placeholder="Escoja un Proveedor",index=None)
st.title("Gestión de Reglas (Descuentos)")
uploaded_rules_file_desc = st.sidebar.file_uploader('Suba archivo de reglas de descuento', type='xlsx',key=st.session_state["uploader_key_desc"])

if 'discount_rules' not in st.session_state:
        st.session_state.discount_rules = pd.DataFrame(columns=[
                'Codigo de Producto',
                'Descuento de Producto',
                'Sucursal',
                ])


if uploaded_rules_file_desc is not None:
    new_rules_df = pd.read_excel(
        uploaded_rules_file_desc,
        dtype={'Codigo de Producto': str,'Sucursal': str},  # Ensure these are text
    )
    required_columns = [
        'Codigo de Producto',
        'Descuento de Producto',
        'Sucursal',
    ]
    if set(new_rules_df.columns) == set(required_columns):        
        # Append the new rules to the session state DataFrame
        st.session_state.discount_rules = pd.concat(
            [st.session_state.discount_rules, new_rules_df],
            ignore_index=True
        )
        
        st.success("Reglas de descuento cargadas correctamente desde el archivo.")
        st.session_state.uploader_key_desc += 1
        st.rerun()
    else:
        difference_columns=np.setdiff1d(required_columns,new_rules_df.columns)
        # Show an error message if columns are missing or extra
        st.error(f"El archivo cargado no contiene las columnas esperadas: {difference_columns}. Descargue el formato para ingresar los datos correctos")

if uploaded_file is None:
        st.warning("◀ Suba un archivo de Excel con la data de ventas para poder continuar.")
st.session_state.discount_rules=st.data_editor(
    st.session_state.discount_rules,
    num_rows='dynamic',
    column_config={
        "Codigo de Producto":st.column_config.TextColumn(),
        "Descuento de Producto":st.column_config.NumberColumn(),
        "Sucursal":st.column_config.ListColumn()
        }
    ,disabled=False)
if uploaded_file is None or monthFile_Desc is None or supplierFile is None or st.session_state.discount_rules is None:
    
    submittedTable = st.button("Mostrar Tabla", disabled=True)
else:
    submittedTable = st.button("Mostrar Tabla", disabled=False,type='primary')
st.sidebar.download_button(label=f'Descargar Formato',data=file_data_d,file_name=st.session_state.file_name_desc,type='primary')

def check_discount_rules(sales_df):
    # Records that do not satisfy the rules
    non_compliant_records = []
    applied_rules = []
    for nro_doc, sale in sales_df.iterrows():
        
        for index, rule in st.session_state.discount_rules.iterrows():
            base_product_codes = rule['Codigo de Producto'].split(',')
            branches = rule['Sucursal'].split(',')
            expected_discount_percentage = rule['Descuento de Producto']

            # Filter sales matching the rule criteria
                
                # Calculate the discount percentage
            total_bruto = float(sale['Total'])
            descuento = float(sale['Dcto'])
            for base_product_code in base_product_codes:
                if total_bruto != 0:  # Avoid division by zero
                    calculated_discount_percentage = int((descuento / (total_bruto+descuento)) * 100)

                    # Check if the calculated discount matches the expected discount
                    if calculated_discount_percentage != expected_discount_percentage:
                        # Add non-compliant record details


                        discount_entry={
                            'Nro Documento': sale['Nro Doc'],  # Include sales document or ID
                            'Sucursal': sale['Sucursal'],
                            'Codigo de Producto': sale['CodigoArt'],
                            'Descuento Esperado%': expected_discount_percentage,
                            'Descuento Actual %': calculated_discount_percentage,
                            'Total Bruto': total_bruto,
                            'Descuento S/.': descuento
                        }
                        if (sale['Nro Doc']) not in applied_rules:
                            non_compliant_records.append(discount_entry)
                            applied_rules.append(sale['Nro Doc'])


    # Create a DataFrame for non-compliant records
    non_compliant_df = pd.DataFrame(non_compliant_records)

    return non_compliant_df.sort_values('Codigo de Producto')


if submittedTable:
    try:
        with st.spinner("Procesando"):
                df = pd.read_excel(uploaded_file,dtype={'Nro Doc': str,'Dcto':float})
                if 'Fecha' in df.columns:
                        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')  # Convert to datetime format
                # Clean the DataFrame by removing rows where 'Tipo Pedido' is NaN
                
                # Filter by 'Proveedor'
                df = df[df['Pro'] == supplierFile]
                # Filter by the selected month in 'Emision'
                df = df[df['Fecha'].dt.month == monthFile_Desc]
                st.subheader(f"Detalle de Ventas del Mes de {monthSelect} ")

                formatedRows=df.copy()
                formatedRows=formatedRows[formatedRows['Dcto'] > 0]
                formatedRows['Fecha'] = formatedRows['Fecha'].dt.strftime('%Y-%m-%d')
                # formatedRows['P unitario'] = formatedRows['P unitario'].apply(lambda x: f"S/ {x:.2f}")
                # #formatedRows['Total Bruto'] = formatedRows['Total Bruto'].apply(lambda x: f"S/ {x:.2f}")
                # formatedRows['Total'] = formatedRows['Total'].apply(lambda x: f"S/ {x:.2f}")
                #formatedRows['Descuento'] = formatedRows['Descuento'].apply(lambda x: f"S/ {x:.2f}")

                st.write(formatedRows)
                st.subheader(f"Detalle de Descuentos del Mes de {monthSelect} ")
                discount_table=check_discount_rules(formatedRows)
                st.write(discount_table)
    except:st.write('No se encontraron descuentos válidos')