import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from time import sleep

st.set_page_config(layout='wide')
submittedTable=None
uploaded_rules_file =None
uploaded_combined_rules_file=None
monthSelect=1
monthFile=None
file_path='Formato de Reglas Bonif.xlsx'
file_path_c='Formato de Reglas Combinadas.xlsx'
with open(file_path, "rb") as file:
    file_data = file.read()
with open(file_path_c, "rb") as file:
    file_data_c = file.read()

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 1

if "comb_uploader_key" not in st.session_state:
    st.session_state["comb_uploader_key"] = 1
if "rule_type_active" not in st.session_state:
    st.session_state.rule_type_active = None
if "file_name_bonf" not in st.session_state:
    st.session_state.file_name_bonf = 'Formato de Reglas Bonif.xlsx'
if 'bonification_rules' not in st.session_state:
        st.session_state.bonification_rules = pd.DataFrame(columns=[
                'Codigo de Producto',
                'Cantidad de Producto',
                'Codigo de Bonificacion',
                'Unidad',
                'Factor',
                'Cantidad de Bonificacion',
                'Costo',
                'Fecha Inicio',
                'Fecha Fin',
                'Sucursal'
                ])

if 'combination_bonification_rules' not in st.session_state:
        st.session_state.combination_bonification_rules = pd.DataFrame(columns=[
                'Codigo de Producto',
                'Cantidad de Producto',
                'Codigo de Bonificacion',
                'Unidad',
                'Factor',
                'Cantidad de Bonificacion',
                'Costo',
                'Fecha Inicio',
                'Fecha Fin',
                'Sucursal'
                ])

# File uploader for Excel
uploaded_file = st.sidebar.file_uploader('Suba el archivo de data general', type='xlsx',label_visibility='collapsed')
#Month select
month_dict = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
monthSelect = st.sidebar.selectbox(
    'Mes', 
    options=list(month_dict.keys()), 
    format_func=lambda name: name, 
    placeholder="Escoja un Mes",index=None
)
if monthSelect is not None:
    monthFile = month_dict[monthSelect]

supplierFile= st.sidebar.selectbox('Proveedor',('AND','ETE','4LO','GUR','PPN','VER','QLP','TCM','PFA','ALT','ADA','BDF','QSZ','COL','ALI','NPU','SAL','K&M','SQL','SAN','ZAI',
'ZUR','NES','UNI','PRY','UNS','FIN','MOL','RSA','COR','COP','GLO','JHO','CDP'),placeholder="Escoja un Proveedor",index=None)

st.title("Gestión de Reglas (Bonificaciones)")
colA,colB,ColC=st.columns(3)
with colA:
    st.session_state.rule_type_active=st.selectbox('Regla a Aplicar',('Regla Simple','Regla Combinada'),index=None,placeholder='Escoja la regla a aplicar')
if st.session_state.rule_type_active is not None:
    if st.session_state.rule_type_active=='Regla Simple':
        st.session_state.file_name_bonf='Formato de Reglas Bonif.xlsx'
        uploaded_rules_file = st.sidebar.file_uploader('Suba archivo de reglas de bonificación (Regla Simple)', type='xlsx',key=st.session_state["uploader_key"])
        st.sidebar.download_button(label=f'Descargar Formato: {st.session_state.rule_type_active}',data=file_data,file_name=st.session_state.file_name_bonf,type='primary')

    elif st.session_state.rule_type_active=='Regla Combinada':
        st.session_state.file_name_bonf='Formato de Reglas Combinadas.xlsx'
        uploaded_combined_rules_file = st.sidebar.file_uploader('Suba archivo de reglas de bonificación (Regla Combinada)', type='xlsx',key=st.session_state["comb_uploader_key"])
        st.sidebar.download_button(label=f'Descargar Formato: {st.session_state.rule_type_active}',data=file_data_c,file_name=st.session_state.file_name_bonf,type='primary')

# If the file is uploaded
if uploaded_file is None:
        st.warning("◀ Suba un archivo de Excel con la data de ventas para poder continuar.")


if uploaded_rules_file is not None:
    
    new_rules_df = pd.read_excel(
        uploaded_rules_file,
        dtype={'Codigo de Producto': str, 'Codigo de Bonificacion': str,'Sucursal': str},  # Ensure these are text
    )
    required_columns = [
        'Codigo de Producto',
        'Cantidad de Producto',
        'Codigo de Bonificacion',
        'Unidad',
        'Factor',
        'Cantidad de Bonificacion',
        'Costo',
        'Fecha Inicio',
        'Fecha Fin',
        'Sucursal'
    ]
    if set(new_rules_df.columns) == set(required_columns):        
        # Append the new rules to the session state DataFrame
        st.session_state.bonification_rules = pd.concat(
            [st.session_state.bonification_rules, new_rules_df],
            ignore_index=True
        )
        
        st.success("Reglas de bonificación cargadas correctamente desde el archivo.")
        st.session_state["uploader_key"] += 1
        st.rerun()
    else:
        difference_columns=np.setdiff1d(required_columns,new_rules_df.columns)
        # Show an error message if columns are missing or extra
        st.error(f"El archivo cargado no contiene las columnas esperadas: {difference_columns}. Descargue el formato para ingresar los datos correctos")

if uploaded_combined_rules_file is not None:
    new_combined_rules_df = pd.read_excel(
        uploaded_combined_rules_file,
        dtype={'Codigo de Producto': str, 'Codigo de Bonificacion': str,'Sucursal': str},  # Ensure these are text
    )
    required_columns = [
        'Codigo de Producto',
        'Cantidad de Producto',
        'Codigo de Bonificacion',
        'Unidad',
        'Factor',
        'Cantidad de Bonificacion',
        'Costo',
        'Fecha Inicio',
        'Fecha Fin',
        'Sucursal'
    ]

    if set(new_combined_rules_df.columns) == set(required_columns):
        st.session_state.combination_bonification_rules = pd.concat(
            [st.session_state.combination_bonification_rules, new_combined_rules_df],
            ignore_index=True
        )
        st.success("Reglas de bonificación cargadas correctamente desde el archivo.")

        st.session_state["comb_uploader_key"] += 1
        st.rerun()
        st.write
    else:
        difference_columns=np.setdiff1d(required_columns,new_combined_rules_df.columns)
        # Show an error message if columns are missing or extra
        st.error(f"El archivo cargado no contiene las columnas esperadas: {difference_columns}. Descargue el formato para ingresar los datos correctos")

if st.session_state.rule_type_active is not None:
    st.subheader(st.session_state.rule_type_active)
st.subheader("Gestor de Reglas")
if st.session_state.rule_type_active=='Regla Simple':
    st.session_state.bonification_rules=st.data_editor(
        st.session_state.bonification_rules,
        num_rows='dynamic',
        column_config={
            "Codigo de Producto":st.column_config.TextColumn(),
            "Cantidad de Producto":st.column_config.NumberColumn(),
            "Codigo de Bonificacion":st.column_config.TextColumn(),
            "Unidad":st.column_config.TextColumn(),
            "Factor":st.column_config.NumberColumn(min_value=1),
            "Cantidad de Bonificacion":st.column_config.NumberColumn(),
            "Costo":st.column_config.NumberColumn(),
            "Fecha Inicio":st.column_config.DateColumn(),
            "Fecha Fin":st.column_config.DateColumn(),
            "Sucursal":st.column_config.ListColumn()
            }
        ,disabled=False)

elif st.session_state.rule_type_active=='Regla Combinada':
    st.session_state.combination_bonification_rules = st.data_editor(
        st.session_state.combination_bonification_rules,
        num_rows='dynamic',
        column_config={
            "Codigo de Producto":st.column_config.TextColumn(),
            "Cantidad de Producto":st.column_config.NumberColumn(),
            "Codigo de Bonificacion":st.column_config.TextColumn(),
            "Unidad":st.column_config.TextColumn(),
            "Factor":st.column_config.NumberColumn(min_value=1),
            "Cantidad de Bonificacion":st.column_config.NumberColumn(),
            "Costo":st.column_config.NumberColumn(),
            "Fecha Inicio":st.column_config.DateColumn(),
            "Fecha Fin":st.column_config.DateColumn(),
            "Sucursal":st.column_config.ListColumn()
            }
        ,disabled=False)

#REGLA SIMPLE#
def apply_bonification_rules_per_sale_simple(sales_df):
    bonification_summary = []

    for nro_doc, group in sales_df.groupby('Nro Documento'):
        applied_rules = []

        for index, rule in st.session_state.bonification_rules.sort_values(by='Cantidad de Producto', ascending=False).iterrows():
            sale_dates = group['Emision'].dt.date.unique()

            for sale_date in sale_dates:
                if (rule['Fecha Inicio'].date() <= sale_date <= rule['Fecha Fin'].date()):
                    # Convert Sucursal back to a string for use in summary and groupby
                    rule['Sucursal'] = ','.join(rule['Sucursal'].split(","))
                    if str(group['Sucursal'].iloc[0]) in rule['Sucursal']:
                        base_product_sales = group[group['Cod. Art.'] == rule['Codigo de Producto']]
                        total_base_quantity = base_product_sales['Cantidad'].sum()
                        bonification_multiplier = total_base_quantity // rule['Cantidad de Producto']

                        if total_base_quantity >= rule['Cantidad de Producto'] and bonification_multiplier > 0 and rule['Codigo de Bonificacion'] not in applied_rules:
                            bonification_product_sales = group[group['Cod. Art.'] == rule['Codigo de Bonificacion']]
                            total_bonification_quantity = bonification_product_sales['Cantidad'].sum()
                            bonification_cost = rule['Costo']
                            factor = rule['Factor']

                            bonification_entry = {
                                'Sucursal': rule['Sucursal'],  # Sucursal is a string here
                                'Nro Documento': nro_doc,
                                'Codigo de Producto': rule['Codigo de Producto'],
                                'Codigo de Bonificacion': rule['Codigo de Bonificacion'],
                                'Quantity': total_bonification_quantity,
                                'Total': (total_bonification_quantity * bonification_cost) / factor,
                                'Costo': bonification_cost,
                                'Mecanica': f"{rule['Cantidad de Producto']} de {rule['Codigo de Producto']}, + {rule['Cantidad de Bonificacion']} de {rule['Codigo de Bonificacion']}",
                                'Factor': factor
                            }

                            bonification_summary.append(bonification_entry)
                            applied_rules.append(rule['Codigo de Bonificacion'])

    bonification_summary_df = pd.DataFrame(bonification_summary)

    # Perform groupby now that Sucursal is a string
    total_bonification_per_rule = bonification_summary_df.groupby(
        ['Sucursal', 'Codigo de Producto', 'Codigo de Bonificacion', 'Mecanica', 'Costo', 'Factor']
    ).agg(
        Cantidad=('Quantity', 'sum'),
        Total=('Total', 'sum'),
    ).reset_index()

    total_bonification_per_rule['Costo'] = total_bonification_per_rule['Costo'].apply(lambda x: f"S/ {x:.2f}")
    total_bonification_per_rule['Total'] = total_bonification_per_rule['Total'].apply(lambda x: f"S/ {x:.2f}")

    # Sort the resulting DataFrame by Sucursal in ascending order
    total_bonification_per_rule = total_bonification_per_rule.sort_values(by='Sucursal', ascending=True).reset_index(drop=True)

    return total_bonification_per_rule


############# Fuera de Regla/Mecanica (Simple)####################

def get_unfulfilled_bonifications_simple(sales_df):
    # Extract records of bonification products where Total Bruto = 0
    unfulfilled_records = []
    applied_rules = set()  # Track processed (Nro Documento, Codigo de Bonificacion)

    for nro_doc, group in sales_df.groupby('Nro Documento'):
        total_bruto_sum = group['Total Bruto'].sum()
        
        for index, rule in st.session_state.bonification_rules.sort_values(by='Cantidad de Producto', ascending=True).iterrows():
            sale_dates = group['Emision'].dt.date.unique()
            
            for sale_date in sale_dates:
                if ((nro_doc, rule['Codigo de Bonificacion']) in applied_rules):
                    # Skip this rule if it's already applied or skipped for the same Nro Documento and Bonificacion
                    continue
                if (rule['Fecha Inicio'].date() <= sale_date <= rule['Fecha Fin'].date()):
                    # Base products and bonification products
                    base_product_sales = group[group['Cod. Art.'] == rule['Codigo de Producto']]
                    bonification_product_sales = group[
                        (group['Cod. Art.'] == rule['Codigo de Bonificacion']) & (group['Total Bruto'] == 0)
                    ]
                    total_base_quantity = base_product_sales['Cantidad'].sum()
                    bonification_product_code = rule['Codigo de Bonificacion']
                    # If total_base_quantity is 0, add a minimal entry without comparison
                    if total_base_quantity == 0 and total_bruto_sum ==0:
                        for _, bonification_row in bonification_product_sales.iterrows():
                            unfulfilled_records_entry = {
                                'Nro Documento': nro_doc,
                                'Sucursal': bonification_row['Sucursal'],  # Include Sucursal
                                'Cantidad Vendida': total_base_quantity,
                                'Cod. Bonificacion': bonification_row['Cod. Art.'],
                                'Cantidad Bonificada': bonification_row['Cantidad'],
                                # Still include the mechanic's quantity
                            }
                            unfulfilled_records.append(unfulfilled_records_entry)
                    # If base quantity is insufficient but there is a bonification product
                    elif total_base_quantity < rule['Cantidad de Producto'] and not bonification_product_sales.empty:
                        for _, bonification_row in bonification_product_sales.iterrows():
                            if (nro_doc, bonification_product_code) not in applied_rules:
                                unfulfilled_records_entry = {
                                    'Nro Documento': nro_doc,
                                    'Sucursal': bonification_row['Sucursal'],  # Include Sucursal
                                    'Cod. Producto': rule['Codigo de Producto'],
                                    'Cantidad Vendida': total_base_quantity,
                                    'Cod. Bonificacion': bonification_row['Cod. Art.'],
                                    'Cantidad Bonificada': bonification_row['Cantidad'],                                    
                                    'Mecanica': f"{rule['Cantidad de Producto']} de {rule['Codigo de Producto']} + {rule['Cantidad de Bonificacion']} de {rule['Codigo de Bonificacion']}"
                                }
                                unfulfilled_records.append(unfulfilled_records_entry)
                    # Mark this `Nro Documento` and `Codigo de Bonificacion` as processed
                    applied_rules.add((nro_doc, bonification_product_code))

    unfulfilled_records_df = pd.DataFrame(unfulfilled_records)

    return unfulfilled_records_df

def get_unfulfilled_bonifications_table_simple(unfulfilled_bonifications_df):
    # Group by 'Codigo de Bonificacion' and calculate the total quantity
    try:
        summary_df = unfulfilled_bonifications_df.groupby(['Cod. Bonificacion','Sucursal']).agg(
            Total_Bonificada=('Cantidad Bonificada', 'sum'),

            
        ).reset_index()

    # Optionally, you can sort the summary by 'Total_Bonificada' in descending order
        summary_df = summary_df.sort_values(by='Total_Bonificada', ascending=False).reset_index(drop=True)

        return summary_df
    except:
        st.warning('No hay Bonificaciones fuera de mecanica')

############# REGLA COMBINADA ###################

def apply_combined_bonification_rule_comb(sales_df):
    bonification_summary = []

    for nro_doc, group in sales_df.groupby('Nro Documento'):
        applied_rules = []

        for index, rule in st.session_state.combination_bonification_rules.iterrows():
            # Dividir los códigos de productos base y bonificación en listas
            base_product_codes = rule['Codigo de Producto'].split(',')
            bonification_product_codes = rule['Codigo de Bonificacion'].split(',')
            total_base_quantity = group[group['Cod. Art.'].isin(base_product_codes)]['Cantidad'].sum()
            if total_base_quantity >= rule['Cantidad de Producto']:
                sale_dates = group['Emision'].dt.date.unique()
                for sale_date in sale_dates:
                    
                    if rule['Fecha Inicio'].date() <= sale_date <= rule['Fecha Fin'].date():
                        rule['Sucursal'] = ','.join(rule['Sucursal'].split(","))
                        if str(group['Sucursal'].iloc[0]) in rule['Sucursal']:
                            bonification_cost = rule['Costo']
                            # Distribuir la cantidad total de bonificación entre los productos de bonificación
                            for bonification_product_code in bonification_product_codes:
                                
                                bonification_product_sales = group[group['Cod. Art.'] == bonification_product_code]
                                total_bonification_quantity = bonification_product_sales['Cantidad'].sum()
                                bonification_entry = {
                                    'Sucursal': rule['Sucursal'],
                                    'Nro Documento': nro_doc,
                                    'Codigo de Producto': ','.join(base_product_codes),
                                    'Codigo de Bonificacion': bonification_product_code,
                                    'Quantity': total_bonification_quantity,
                                    'Total': (total_bonification_quantity * bonification_cost)/rule['Factor'],
                                    'Costo': rule['Costo'],
                                    'Mecanica': f"{rule['Cantidad de Producto']} de {' y/o '.join(base_product_codes)} + {rule['Cantidad de Bonificacion']} de {bonification_product_code}",
                                    'Factor': rule['Factor']
                                }

                                # Agregar solo si aún no se ha aplicado esta combinación en este documento
                                if (nro_doc, bonification_product_code) not in applied_rules:
                                    bonification_summary.append(bonification_entry)
                                    applied_rules.append((nro_doc, bonification_product_code))
    
    # Convertir el resumen de bonificaciones en un DataFrame
    bonification_summary_df = pd.DataFrame(bonification_summary)

    # Agregar totales de cantidad y valor por regla
    total_bonification_per_rule = bonification_summary_df.groupby(
        ['Sucursal','Codigo de Producto', 'Codigo de Bonificacion', 'Mecanica', 'Costo', 'Factor']
    ).agg(
        Cantidad=('Quantity', 'sum'),
        Total=('Total', 'sum'),
    ).reset_index()
    total_bonification_per_rule['Costo'] = total_bonification_per_rule['Costo'].apply(lambda x: f"S/ {x:.2f}")

    total_bonification_per_rule['Total'] = total_bonification_per_rule['Total'].apply(lambda x: f"S/ {x:.2f}")

    return total_bonification_per_rule

############# Fuera de Regla ####################
def get_unfulfilled_bonifications_comb(sales_df):
    unfulfilled_records = []  # List to store records that don't fulfill the rule
    applied_rules = set() 
    # Iterate over each sale document
    for nro_doc, group in sales_df.groupby('Nro Documento'):

        # Track bonification product entries with Total Bruto = 0
        for index, rule in st.session_state.combination_bonification_rules.iterrows():
            # Check if the sale is within the rule's date range
            sale_dates = group['Emision'].dt.date.unique()
            for sale_date in sale_dates:
                if rule['Fecha Inicio'].date() <= sale_date <= rule['Fecha Fin'].date():

                    # Filter for base products and bonification products in the sale
                    base_product_sales = group[group['Cod. Art.'].isin(rule['Codigo de Producto'].split(','))]
                    bonification_product_sales = group[
                        (group['Cod. Art.'].isin(rule['Codigo de Bonificacion'].split(','))) & (group['Total Bruto'] == 0)
                    ]

                    # Calculate the total base quantity in this sale
                    total_base_quantity = base_product_sales['Cantidad'].sum()

                    # Check if the sale meets the base quantity requirement
                    if total_base_quantity < rule['Cantidad de Producto'] and not bonification_product_sales.empty:
                        # Append each bonification product record that doesn't fulfill the rule
                        for _, bonification_row in bonification_product_sales.iterrows():
                            unfulfilled_records.append({
                                'Nro Documento': nro_doc,
                                'Cod. Producto': rule['Codigo de Producto'],
                                'Cantidad Vendida': total_base_quantity,
                                'Cod. Bonificacion': bonification_row['Cod. Art.'],
                                'Cantidad Bonificada': bonification_row['Cantidad'],
                                'Mecanica': f"{rule['Cantidad de Producto']} de {rule['Codigo de Producto']} + {rule['Cantidad de Bonificacion']} de {rule['Codigo de Bonificacion']}"
                            })

    # Convert the unfulfilled records list to a DataFrame
    unfulfilled_records_df = pd.DataFrame(unfulfilled_records)
    return unfulfilled_records_df


if uploaded_file is None or monthFile is None or supplierFile is None or st.session_state.rule_type_active is None:
    
    submittedTable = st.button("Mostrar Tabla", disabled=True)

elif (st.session_state.rule_type_active=='Regla Simple' and st.session_state.bonification_rules.empty==False) or (st.session_state.rule_type_active=='Regla Combinada' and st.session_state.combination_bonification_rules.empty==False):
    submittedTable = st.button("Mostrar Tabla", disabled=False,type='primary')


if submittedTable:
    try:
        with st.spinner("Procesando"):
                df = pd.read_excel(uploaded_file,dtype={'Nro Documento': str, 'Cod. Cliente': str,'RUC/DNI': str})
                if 'Emision' in df.columns:
                        df['Emision'] = pd.to_datetime(df['Emision'], errors='coerce')  # Convert to datetime format
                # Clean the DataFrame by removing rows where 'Tipo Pedido' is NaN
                if 'Tipo Pedido' in df.columns:
                    df = df.dropna(subset=['Tipo Pedido'])
                # Filter by 'Proveedor'
                dfProvider = df[df['Proveedor'] == supplierFile]
                # Filter by the selected month in 'Emision'
                month_rows = dfProvider[dfProvider['Emision'].dt.month == monthFile]
                st.subheader(f"Detalle de Venta del Mes de {monthSelect} ")

                formatedRows=month_rows.copy()

                formatedRows['Emision'] = formatedRows['Emision'].dt.strftime('%Y-%m-%d')
                formatedRows['P. Unitario'] = formatedRows['P. Unitario'].apply(lambda x: f"S/ {x:.2f}")
                formatedRows['Total Bruto'] = formatedRows['Total Bruto'].apply(lambda x: f"S/ {x:.2f}")
                formatedRows['Total'] = formatedRows['Total'].apply(lambda x: f"S/ {x:.2f}")
                formatedRows['Descuento'] = formatedRows['Descuento'].apply(lambda x: f"S/ {x:.2f}")

                st.write(formatedRows)
                if st.session_state.rule_type_active=='Regla Simple':
                    bonificationTable = apply_bonification_rules_per_sale_simple(month_rows)
                    
                    unfulfilledBonifications = get_unfulfilled_bonifications_simple(month_rows)
                    unfulfilledBonifications_table = get_unfulfilled_bonifications_table_simple(unfulfilledBonifications)
                elif st.session_state.rule_type_active=='Regla Combinada':
                    bonificationTable = apply_combined_bonification_rule_comb(month_rows)
                    unfulfilledBonifications = get_unfulfilled_bonifications_comb(month_rows)
                    unfulfilledBonifications_table = get_unfulfilled_bonifications_table_simple(unfulfilledBonifications)
                st.title(f"Resumen de Bonificaciones por Mecánica: {st.session_state.rule_type_active}")
                st.write(bonificationTable)
                st.title(f"Bonificaciones fuera de Mecánica: {st.session_state.rule_type_active}")
                st.write(unfulfilledBonifications)
                st.write(unfulfilledBonifications_table)
    except:st.write('No se encontraron bonificaciones válidas')


