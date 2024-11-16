import streamlit as st
import pandas as pd
from datetime import datetime
from time import sleep

st.set_page_config(layout='wide')
submittedTable=None
uploaded_rules_file =None
uploaded_combined_rules_file=None
monthSelect=1
monthFile=None
file_path='Formato_bonf_rules.xlsx'
with open(file_path, "rb") as file:
    file_data = file.read()
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 1
if "edit_indices" not in st.session_state:
    st.session_state["edit_indices"] = 1
if "comb_uploader_key" not in st.session_state:
    st.session_state["comb_uploader_key"] = 1

# File uploader for Excel
uploaded_file = st.sidebar.file_uploader('Suba un archivo del Detalle de Venta', type='xlsx')
month_dict = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}

monthSelect = st.sidebar.selectbox(
    'Mes', 
    options=list(month_dict.keys()), 
    format_func=lambda name: name, 
    placeholder="Escoja un Mes",index=None
)
if monthSelect is not None:
    monthFile = month_dict[monthSelect]

supplierFile= st.sidebar.selectbox('Proveedor',('ETE','4LO','AND','GUR','PPN','VER'),placeholder="Escoja un Proveedor",index=None)
st.title("Gestión de Reglas")

registro_regla=st.selectbox('Regla a Aplicar',('Regla Simple','Regla Combinada'),index=None,placeholder='Escoja la regla a aplicar')
if registro_regla is not None:
    if registro_regla=='Regla Simple':
        uploaded_rules_file = st.sidebar.file_uploader('Suba archivo de reglas de bonificación (Regla Simple)', type='xlsx',key=st.session_state["uploader_key"])
    elif registro_regla=='Regla Combinada':
        uploaded_combined_rules_file = st.sidebar.file_uploader('Suba archivo de reglas de bonificación (Regla Combinada)', type='xlsx',key=st.session_state["comb_uploader_key"])
# If the file is uploaded
if uploaded_file is None:
        st.write("Suba un archivo de Excel primero para poder continuar.")

st.sidebar.download_button(label='Formato de archivo de reglas de bonificación',data=file_data,file_name='Formato de Reglas Bonif.xlsx')
# Initialize bonification rules DataFrame in session state
if 'bonification_rules' not in st.session_state:
        st.session_state['bonification_rules'] = pd.DataFrame(columns=[
                'Codigo de Producto',
                'Cantidad de Producto',
                'Codigo de Bonificacion',
                'Unidad',
                'Cantidad de Bonificacion',
                'Costo',
                'Fecha Inicio',
                'Fecha Fin',
                'Estado'
                ])
bonification_rules = st.session_state['bonification_rules']

if 'combination_bonification_rules' not in st.session_state:
        st.session_state['combination_bonification_rules'] = pd.DataFrame(columns=[
                'Codigo de Producto',
                'Cantidad de Producto',
                'Codigo de Bonificacion',
                'Unidad',
                'Cantidad de Bonificacion',
                'Costo',
                'Fecha Inicio',
                'Fecha Fin',
                'Estado'
                ])
combination_bonification_rules = st.session_state['combination_bonification_rules']

if 0 in bonification_rules.index:
    bonification_rules.index=bonification_rules.index+1
if 0 in combination_bonification_rules.index:
    combination_bonification_rules.index=combination_bonification_rules.index+1
if uploaded_rules_file is not None:
    
    new_rules_df = pd.read_excel(
        uploaded_rules_file,
        dtype={'Codigo de Producto': str, 'Codigo de Bonificacion': str},  # Ensure these are text
    )
    new_rules_df['Estado'] = 'Activo'
    st.session_state['bonification_rules'] = pd.concat(
        [st.session_state['bonification_rules'], new_rules_df],
        ignore_index=True
    )
    
    st.success("Reglas de bonificación cargadas correctamente desde el archivo.")

    st.session_state["uploader_key"] += 1
    st.rerun()
    st.write

if uploaded_combined_rules_file is not None:
    new_combined_rules_df = pd.read_excel(
        uploaded_combined_rules_file,
        dtype={'Codigo de Producto': str, 'Codigo de Bonificacion': str},  # Ensure these are text
    )
    new_combined_rules_df['Estado'] = 'Activo'
    st.session_state['combination_bonification_rules'] = pd.concat(
        [st.session_state['combination_bonification_rules'], new_combined_rules_df],
        ignore_index=True
    )
    
    st.success("Reglas de bonificación cargadas correctamente desde el archivo.")

    st.session_state["comb_uploader_key"] += 1
    st.rerun()
    st.write




def add_bonification_rule(base_product_code, base_product_quantity, bonification_product_code, bonification_product_unit, bonification_quantity, cost, start_date, end_date):
    global bonification_rules
    new_rule = pd.DataFrame({
        'Codigo de Producto': [base_product_code],
        'Cantidad de Producto': [base_product_quantity],
        'Codigo de Bonificacion': [bonification_product_code],
        'Unidad de Bonificacion':[bonification_product_unit],
        'Cantidad de Bonificacion': [bonification_quantity],
        'Costo': [cost],
        'Fecha Inicio': [pd.to_datetime(start_date)],
        'Fecha Fin': [pd.to_datetime(end_date)],
        'Estado': 'Activo'
    })
    st.session_state['bonification_rules'] = pd.concat([bonification_rules, new_rule], ignore_index=True)
    st.rerun()
    st.success("Regla registrada correctamente!")

def add_combination_bonification_rule(base_product_code, base_product_quantity, bonification_product_code, bonification_product_unit, bonification_quantity, cost, start_date, end_date):
    global combination_bonification_rules
    new_combination_rule = pd.DataFrame({
        'Codigo de Producto': [base_product_code],
        'Cantidad de Producto': [base_product_quantity],
        'Codigo de Bonificacion': [bonification_product_code],
        'Unidad de Bonificacion':[bonification_product_unit],
        'Cantidad de Bonificacion': [bonification_quantity],
        'Costo': [cost],
        'Fecha Inicio': [pd.to_datetime(start_date)],  # Convert to datetime
        'Fecha Fin': [pd.to_datetime(end_date)],       # Convert to datetime
        'Estado': 'Activo'
    })
    st.session_state['combination_bonification_rules'] = pd.concat([combination_bonification_rules, new_combination_rule], ignore_index=True)
    st.rerun()
    st.success("Regla registrada correctamente!")

# Function to delete bonification rules based on indices
def delete_bonification_rule(indices):
    global bonification_rules
    bonification_rules = bonification_rules.drop(indices).reset_index(drop=True)
    st.session_state['bonification_rules'] = bonification_rules
    st.rerun()

def delete_combination_bonification_rule(indices):
    global combination_bonification_rules
    combination_bonification_rules = combination_bonification_rules.drop(indices).reset_index(drop=True)
    st.session_state['combination_bonification_rules'] = combination_bonification_rules
    st.rerun()


if registro_regla=='Regla Simple':
        st.subheader("Regla Simple")
elif registro_regla=='Regla Combinada':
        st.subheader("Regla Combinada")
if registro_regla is not None:
    with st.form("bonification_rule_form"):
            base_product_code = st.text_input("Código de Producto Base")
            base_product_quantity = st.number_input("Cantidad de Producto Base", min_value=1)
            bonification_product_code = st.text_input("Código de Producto de Bonificación")
            bonification_product_unit = st.text_input("Unidad de Producto de Bonificación")
            bonification_quantity = st.number_input("Cantidad de Producto de Bonificación", min_value=1)
            cost = st.number_input("Costo", min_value=0.0, format="%.2f")
            start_date = st.date_input("Fecha de Inicio", value=datetime.today())
            end_date = st.date_input("Fecha Final", value=datetime.today())

            # Submit button
            submitted = st.form_submit_button("Agregar Regla")

            if submitted:
                    if registro_regla=='Regla Simple':
                            add_bonification_rule(base_product_code, base_product_quantity, bonification_product_code,bonification_product_unit, bonification_quantity, cost, start_date, end_date)
                            
                    elif registro_regla=='Regla Combinada':
                            add_combination_bonification_rule(base_product_code, base_product_quantity, bonification_product_code,bonification_product_unit, bonification_quantity, cost, start_date, end_date)

                    

# Display the DataFrame with a checkbox to select rows for deletion
st.subheader("Reglas Registradas")
if registro_regla=='Regla Simple':
    if not bonification_rules.empty:
        delete_indices = st.multiselect("Seleccione las reglas a Eliminar", bonification_rules.index, format_func=lambda x: f"Regla {x}", placeholder='Escoja una regla')

        if st.button("Borrar regla seleccionada"):
            delete_bonification_rule(delete_indices)
            st.success(f"Regla(s) Eliminadas(s): {', '.join(map(str, delete_indices))}")

        st.write(bonification_rules)

        edit_indices = st.selectbox("Seleccione la regla a Modificar", bonification_rules.index, format_func=lambda x: f"Regla {x}", placeholder='Escoja una regla',index=st.session_state['edit_indices'])
        if edit_indices!=None:
            with st.form(key="edit_rule_form"):
                st.write(f"Editando la regla {edit_indices}")

                base_product_code = st.text_input("Código de Producto Base", bonification_rules.loc[edit_indices, 'Codigo de Producto'])
                base_product_quantity = st.number_input("Cantidad de Producto Base", value=bonification_rules.loc[edit_indices, 'Cantidad de Producto'], step=1)
                bonification_product_code = st.text_input("Código de Producto de Bonificación", bonification_rules.loc[edit_indices, 'Codigo de Bonificacion'])
                bonification_product_unit = st.text_input("Unidad de Producto de Bonificación", bonification_rules.loc[edit_indices, 'Unidad'])
                bonification_quantity = st.number_input("Cantidad de Producto de Bonificación", value=bonification_rules.loc[edit_indices, 'Cantidad de Bonificacion'], step=1)
                cost = st.number_input("Costo", value=bonification_rules.loc[edit_indices, 'Costo'], step=0.01)
                start_date = st.date_input("Fecha de Inicio", bonification_rules.loc[edit_indices, 'Fecha Inicio'])
                end_date = st.date_input("Fecha Final", bonification_rules.loc[edit_indices, 'Fecha Fin'])
                estado = st.selectbox("Estado", options=['Activo', 'Inactivo'], index=0 if bonification_rules.loc[edit_indices, 'Estado'] == 'Activo' else 1)
                
                submittedEdit = st.form_submit_button("Guardar cambios")
                with st.spinner('Actualizando'):
                    if submittedEdit:
                        # Actualizar el DataFrame con los valores editados
                        bonification_rules.loc[edit_indices, 'Codigo de Producto'] = base_product_code
                        bonification_rules.loc[edit_indices, 'Cantidad de Producto'] = base_product_quantity
                        bonification_rules.loc[edit_indices, 'Codigo de Bonificacion'] = bonification_product_code
                        bonification_rules.loc[edit_indices, 'Unidad'] = bonification_product_unit
                        bonification_rules.loc[edit_indices, 'Cantidad de Bonificacion'] = bonification_quantity
                        bonification_rules.loc[edit_indices, 'Costo'] = cost
                        bonification_rules.loc[edit_indices, 'Fecha Inicio'] = pd.to_datetime(start_date)
                        bonification_rules.loc[edit_indices, 'Fecha Fin'] = pd.to_datetime(end_date)
                        bonification_rules.loc[edit_indices, 'Estado'] = estado
                        
                        st.success(f"Regla {edit_indices} actualizada con éxito.")

    else:
        st.write("Sin Reglas Registradas.")
elif registro_regla=='Regla Combinada':
    if not combination_bonification_rules.empty:
        delete_indices = st.multiselect("Seleccione las reglas a Eliminar", combination_bonification_rules.index, format_func=lambda x: f"Regla {x}", placeholder='Escoja una regla')

        if st.button("Borrar regla seleccionada"):
            delete_combination_bonification_rule(delete_indices)
            st.success(f"Regla(s) Eliminadas(s): {', '.join(map(str, delete_indices))}")

        st.write(combination_bonification_rules)
    else:
        st.write("Sin Reglas Registradas.")

############## REGLA SIMPLE #####################

def apply_bonification_rules_per_sale2(sales_df):
    bonification_summary = []

    for nro_doc, group in sales_df.groupby('Pedido'):
        applied_rules = []

        for index, rule in bonification_rules.sort_values(by='Cantidad de Producto', ascending=False).iterrows():
            sale_dates = group['Emision'].dt.date.unique()
            for sale_date in sale_dates:
                if rule['Fecha Inicio'].date() <= sale_date <= rule['Fecha Fin'].date():
                    base_product_sales = group[group['Cod. Art.'] == rule['Codigo de Producto']]
                    total_base_quantity = base_product_sales['Cantidad'].sum()
                    bonification_multiplier = total_base_quantity // rule['Cantidad de Producto']

                    if total_base_quantity >= rule['Cantidad de Producto'] and bonification_multiplier > 0 and rule['Codigo de Bonificacion'] not in applied_rules:
                        bonification_product_sales = group[group['Cod. Art.'] == rule['Codigo de Bonificacion']]
                        total_bonification_quantity = bonification_product_sales['Cantidad'].sum()
                        bonification_cost = rule['Costo']

                        bonification_entry = {
                            'Nro Documento': nro_doc,
                            'Codigo de Producto': rule['Codigo de Producto'],
                            'Codigo de Bonificacion': rule['Codigo de Bonificacion'],
                            'Quantity': total_bonification_quantity,
                            'Total': total_bonification_quantity * bonification_cost,
                            'Costo': bonification_cost,
                            'Regla': f"{rule['Codigo de Bonificacion']} (Compra {rule['Cantidad de Producto']} de {rule['Codigo de Producto']}, de Regalo {rule['Cantidad de Bonificacion']} de {rule['Codigo de Bonificacion']})"
                        }

                        bonification_summary.append(bonification_entry)
                        applied_rules.append(rule['Codigo de Bonificacion'])

    bonification_summary_df = pd.DataFrame(bonification_summary)

    total_bonification_per_rule = bonification_summary_df.groupby(
        ['Codigo de Producto', 'Codigo de Bonificacion', 'Regla', 'Costo']
    ).agg(
        Cantidad=('Quantity', 'sum'),
        Total=('Total', 'sum'),
    ).reset_index()

    total_bonification_per_rule['Costo'] = total_bonification_per_rule['Costo'].apply(lambda x: f"S/ {x:.2f}")

    total_bonification_per_rule['Total'] = total_bonification_per_rule['Total'].apply(lambda x: f"S/ {x:.2f}")

    return total_bonification_per_rule
############# Fuera de Regla ####################
def get_unfulfilled_bonifications(sales_df):
    unfulfilled_records = []  # List to store records that don't fulfill the rule

    # Iterate over each sale document
    for nro_doc, group in sales_df.groupby('Pedido'):

        # Track bonification product entries with Total Bruto = 0
        for index, rule in combination_bonification_rules.iterrows():
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
                                'Codigo de Producto': rule['Codigo de Producto'],
                                'Codigo de Bonificacion': bonification_row['Cod. Art.'],
                                'Cantidad': bonification_row['Cantidad'],
                                'Total Bruto': bonification_row['Total Bruto'],
                                'Rule_Required_Base_Quantity': rule['Cantidad de Producto'],
                                'Actual_Base_Quantity': total_base_quantity
                            })

    # Convert the unfulfilled records list to a DataFrame
    unfulfilled_records_df = pd.DataFrame(unfulfilled_records)
    return unfulfilled_records_df

############# REGLA COMBINADA ###################

def apply_combined_bonification_rule2(sales_df):
    bonification_summary = []

    for nro_doc, group in sales_df.groupby('Pedido'):
        applied_rules = []

        for index, rule in combination_bonification_rules.iterrows():
            # Dividir los códigos de productos base y bonificación en listas
            base_product_codes = rule['Codigo de Producto'].split(',')
            bonification_product_codes = rule['Codigo de Bonificacion'].split(',')
            total_base_quantity = group[group['Cod. Art.'].isin(base_product_codes)]['Cantidad'].sum()
            if total_base_quantity >= rule['Cantidad de Producto']:
                sale_dates = group['Emision'].dt.date.unique()
                for sale_date in sale_dates:
                    print(sale_date)
                    print(rule['Fecha Inicio'].date())
                    print(rule['Fecha Inicio'].date())
                    if rule['Fecha Inicio'].date() <= sale_date <= rule['Fecha Fin'].date():
                        bonification_cost = rule['Costo']
                        # Distribuir la cantidad total de bonificación entre los productos de bonificación
                        for bonification_product_code in bonification_product_codes:
                            print(bonification_product_code)
                            bonification_product_sales = group[group['Cod. Art.'] == bonification_product_code]
                            total_bonification_quantity = bonification_product_sales['Cantidad'].sum()
                            bonification_entry = {
                                'Nro Documento': nro_doc,
                                'Codigo de Producto': ','.join(base_product_codes),
                                'Codigo de Bonificacion': bonification_product_code,
                                'Quantity': total_bonification_quantity,
                                'Total': total_bonification_quantity * bonification_cost,
                                'Costo': bonification_cost,
                                'Regla': f"{bonification_product_code} (Compra {rule['Cantidad de Producto']} de {', '.join(base_product_codes)}, de Regalo {rule['Cantidad de Bonificacion']} de {bonification_product_code})"
                            }

                            # Agregar solo si aún no se ha aplicado esta combinación en este documento
                            if (nro_doc, bonification_product_code) not in applied_rules:
                                bonification_summary.append(bonification_entry)
                                applied_rules.append((nro_doc, bonification_product_code))
    
    # Convertir el resumen de bonificaciones en un DataFrame
    bonification_summary_df = pd.DataFrame(bonification_summary)

    # Agregar totales de cantidad y valor por regla
    total_bonification_per_rule = bonification_summary_df.groupby(
        ['Codigo de Producto', 'Codigo de Bonificacion', 'Regla', 'Costo']
    ).agg(
        Cantidad=('Quantity', 'sum'),
        Total=('Total', 'sum'),
    ).reset_index()
    total_bonification_per_rule['Costo'] = total_bonification_per_rule['Costo'].apply(lambda x: f"S/ {x:.2f}")

    total_bonification_per_rule['Total'] = total_bonification_per_rule['Total'].apply(lambda x: f"S/ {x:.2f}")

    return total_bonification_per_rule
############# Fuera de Regla ####################
def get_unfulfilled_bonifications_v2(sales_df):
    # Run the bonification rule application to get all fulfilled rules
    fulfilled_rules_df = apply_bonification_rules_per_sale2(sales_df)

    # Extract records of bonification products where Total Bruto = 0
    unfulfilled_records = []

    for nro_doc, group in sales_df.groupby('Pedido'):
        for index, rule in bonification_rules.iterrows():
            sale_dates = group['Emision'].dt.date.unique()

            for sale_date in sale_dates:
                if rule['Fecha Inicio'].date() <= sale_date <= rule['Fecha Fin'].date():
                    # Base products and bonification products
                    base_product_sales = group[group['Cod. Art.'] == rule['Codigo de Producto']]
                    bonification_product_sales = group[
                        (group['Cod. Art.'] == rule['Codigo de Bonificacion']) & (group['Total Bruto'] == 0)
                    ]

                    total_base_quantity = base_product_sales['Cantidad'].sum()

                    # Check if it does NOT meet the bonification rule but has a bonification product
                    if total_base_quantity < rule['Cantidad de Producto'] and not bonification_product_sales.empty:
                        for _, bonification_row in bonification_product_sales.iterrows():
                            unfulfilled_records.append({
                                'Nro Documento': nro_doc,
                                'Codigo de Producto': rule['Codigo de Producto'],
                                'Codigo de Bonificacion': bonification_row['Cod. Art.'],
                                'Quantity': bonification_row['Cantidad'],
                                'Total Bruto': bonification_row['Total Bruto'],
                                'Required_Base_Quantity': rule['Cantidad de Producto'],
                                'Actual_Base_Quantity': total_base_quantity
                            })

    unfulfilled_records_df = pd.DataFrame(unfulfilled_records)
    return unfulfilled_records_df

if uploaded_file is None or monthFile is None or supplierFile is None or registro_regla is None:

    submittedTable = st.button("Mostrar Tabla", disabled=True)

elif (registro_regla=='Regla Simple' and bonification_rules.empty==False) or (registro_regla=='Regla Combinada' and combination_bonification_rules.empty==False):
    submittedTable = st.button("Mostrar Tabla", disabled=False)

if submittedTable:
    try:
        with st.spinner("Procesando"):
                df = pd.read_excel(uploaded_file,dtype={'Pedido': str, 'Cod. Cliente': str,'RUC/DNI': str})
                if 'Emision' in df.columns:
                        df['Emision'] = pd.to_datetime(df['Emision'], errors='coerce')  # Convert to datetime format

                # Clean the DataFrame by removing rows where 'Tipo Pedido' is NaN
                df_dropNull = df.dropna(subset=['Tipo Pedido'])

                # # Drop unnecessary columns
                # df_cutColumns = df_dropNull.drop(['TD', 'Cod. Ruteo', 'RUC/DNI'], axis=1)

                # Filter by 'Proveedor' = 'ETE'
                dfProvider = df_dropNull[df_dropNull['Proveedor'] == supplierFile]

                # Filter by the selected month in 'Emision'
                month_rows = dfProvider[dfProvider['Emision'].dt.month == monthFile]

                # Display the filtered DataFrame
                st.subheader(f"Detalle de Venta del Mes de {monthSelect}")
                
                formatedRows=month_rows.copy()

                formatedRows['Emision'] = formatedRows['Emision'].dt.strftime('%Y-%m-%d')
                formatedRows['P. Unitario'] = formatedRows['P. Unitario'].apply(lambda x: f"S/ {x:.2f}")
                formatedRows['Total Bruto'] = formatedRows['Total Bruto'].apply(lambda x: f"S/ {x:.2f}")
                formatedRows['Total'] = formatedRows['Total'].apply(lambda x: f"S/ {x:.2f}")
                formatedRows['Descuento'] = formatedRows['Descuento'].apply(lambda x: f"S/ {x:.2f}")

                st.write(formatedRows)
        if registro_regla=='Regla Simple':
            bonificationTable = apply_bonification_rules_per_sale2(month_rows)
            unfulfilledBonifications = get_unfulfilled_bonifications_v2(month_rows)
        elif registro_regla=='Regla Combinada':
            bonificationTable = apply_combined_bonification_rule2(month_rows)
            unfulfilledBonifications = get_unfulfilled_bonifications(month_rows)
        st.title(f"Resumen de Bonificaciones: {registro_regla}")
        with st.spinner("Procesando"):
            sleep(1)
            st.write(bonificationTable)
        
        st.title(f"Bonificaciones sin Regla: {registro_regla}")
        with st.spinner("Procesando"):
            sleep(1)
            st.write(unfulfilledBonifications)
    except:
        st.write('No se encontraron bonificaciones válidas')
