import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from time import sleep
st.set_page_config(layout='wide')

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 1

# File uploader for Excel
uploaded_file = st.sidebar.file_uploader('Suba el archivo de data general', type='xlsx',label_visibility='collapsed')
if uploaded_file is None:
        st.write("Suba un archivo de Excel primero para poder continuar.")
month_dict = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}

monthSelect = st.sidebar.selectbox(
    'Mes', 
    options=list(month_dict.keys()), 
    format_func=lambda name: name, 
    placeholder="Escoja un Mes",index=None
)
if monthSelect is not None:
    monthFile = month_dict[monthSelect]

supplierFile= st.sidebar.selectbox('Proveedor',('ETE','4LO','AND','GUR','PPN','VER','QLP'),placeholder="Escoja un Proveedor",index=None)
st.title("Gestión de Reglas")
uploaded_rules_file = st.sidebar.file_uploader('Suba archivo de reglas de bonificación (Regla Simple)', type='xlsx',key=st.session_state["uploader_key"])

if 'discount_rules' not in st.session_state:
        st.session_state['discount_rules'] = pd.DataFrame(columns=[
                'Codigo de Producto',
                'Descuento de Producto',
                'Sucursal',
                'Estado'
                ])
discount_rules = st.session_state['discount_rules']
if 0 in discount_rules.index:
    discount_rules.index=discount_rules.index+1

if uploaded_rules_file is not None:
    
    new_rules_df = pd.read_excel(
        uploaded_rules_file,
        dtype={'Codigo de Producto': str},
    )
    new_rules_df['Estado'] = 'Activo'
    st.session_state['discount_rules'] = pd.concat(
        [st.session_state['discount_rules'], new_rules_df],
        ignore_index=True
    )
    
    st.success("Reglas de descuento cargadas correctamente desde el archivo.")

    st.session_state["uploader_key"] += 1
    st.rerun()
    st.write


def add_discount_rules(base_product_code, product_discount, branch):
    global discount_rules
    new_rule = pd.DataFrame({
        'Codigo de Producto': [base_product_code],
        'Descuento de Producto': [product_discount],
        'Sucursal': [branch],
        'Estado': 'Activo'
    })
    st.session_state['discount_rules'] = pd.concat([discount_rules, new_rule], ignore_index=True)
    st.rerun()
    st.success("Regla registrada correctamente!")
def delete_discount_rules(indices):
    global discount_rules
    discount_rules = discount_rules.drop(indices).reset_index(drop=True)
    st.session_state['discount_rules'] = discount_rules
    st.rerun()

with st.form("discount_rule_form"):
    base_product_code = st.text_input("Codigo de Producto")
    product_discount = st.number_input("Descuento de Producto (%)", min_value=1)
    branch = st.text_input("Sucursal")

            # Submit button
    submitted = st.form_submit_button("Agregar Regla")
    if submitted:
        add_discount_rules(base_product_code, product_discount, branch)
st.subheader("Reglas Registradas")

if not discount_rules.empty:
        delete_indices = st.multiselect("Seleccione las reglas a Eliminar", discount_rules.index, format_func=lambda x: f"Regla {x}", placeholder='Escoja una regla')

        if st.button("Borrar regla seleccionada"):
            delete_discount_rules(delete_indices)
            st.success(f"Regla(s) Eliminadas(s): {', '.join(map(str, delete_indices))}")

        st.write(discount_rules)

        edit_indices = st.selectbox("Seleccione la regla a Modificar", discount_rules.index, format_func=lambda x: f"Regla {x}", placeholder='Escoja una regla',index=None)
        if edit_indices!=None:
            with st.form(key="edit_rule_form"):
                st.write(f"Editando la regla {edit_indices}")

                base_product_code = st.text_input("Codigo de Producto", discount_rules.loc[edit_indices, 'Codigo de Producto'])
                product_discount = st.number_input("Descuento de Producto (%)", value=discount_rules.loc[edit_indices, 'Descuento de Producto'], step=1)
                branch = st.text_input("Sucursal", discount_rules.loc[edit_indices, 'Sucursal'])                
                estado = st.selectbox("Estado", options=['Activo', 'Inactivo'], index=0 if discount_rules.loc[edit_indices, 'Estado'] == 'Activo' else 1)
                
                submittedEdit = st.form_submit_button("Guardar cambios")
                with st.spinner('Actualizando'):
                    if submittedEdit:
                        # Actualizar el DataFrame con los valores editados
                        discount_rules.loc[edit_indices, 'Codigo de Producto'] = base_product_code
                        discount_rules.loc[edit_indices, 'Descuento de Producto'] = product_discount
                        discount_rules.loc[edit_indices, 'Sucursal'] = branch
                        discount_rules.loc[edit_indices, 'Estado'] = estado
                        
                        st.success(f"Regla {edit_indices} actualizada con éxito.")
else:
    st.write("Sin Reglas Registradas.")


def apply_discount_rules(discount_df):
    discount_summary = []
    onlyDiscounts = discount_df[discount_df['Descuento'] != 0]

    for sale, index in onlyDiscounts:
        for index, rule in discount_rules:
            base_product_sales = group[group['Cod. Art.'] == rule['Codigo de Producto']]
            if (sale['Descuento']/sale['Total Bruto']) != rule['Descuento de Producto']:
                discount_entry = {
                            'Nro Documento': nro_doc,
                            'Codigo de Producto': rule['Codigo de Producto'],
                            'Codigo de Bonificacion': rule['Codigo de Bonificacion'],
                            'Quantity': total_bonification_quantity,
                            'Total': total_bonification_quantity * bonification_cost,
                            'Costo': bonification_cost,
                            'Regla': f"{rule['Codigo de Bonificacion']} (Compra {rule['Cantidad de Producto']} de {rule['Codigo de Producto']}, de Regalo {rule['Cantidad de Bonificacion']} de {rule['Codigo de Bonificacion']})"
                        }
    for nro_doc, group in discount_df.groupby('Pedido'):
        for index, rule in discount_rules.sort_values(by='Cantidad de Producto', ascending=False).iterrows():
            sale_dates = group['Emision'].dt.date.unique()
            for sale_date in sale_dates:
                if rule['Fecha Inicio'].date() <= sale_date <= rule['Fecha Fin'].date():
                    base_product_sales = group[group['Cod. Art.'] == rule['Codigo de Producto']]
                    total_base_quantity = base_product_sales['Cantidad'].sum()
                    bonification_multiplier = total_base_quantity // rule['Cantidad de Producto']

                    if total_base_quantity >= rule['Cantidad de Producto'] and bonification_multiplier > 0:
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

                        discount_summary.append(bonification_entry)
                        

    bonification_summary_df = pd.DataFrame(discount_summary)

    total_bonification_per_rule = bonification_summary_df.groupby(
        ['Codigo de Producto', 'Codigo de Bonificacion', 'Regla', 'Costo']
    ).agg(
        Cantidad=('Quantity', 'sum'),
        Total=('Total', 'sum'),
    ).reset_index()

    total_bonification_per_rule['Costo'] = total_bonification_per_rule['Costo'].apply(lambda x: f"S/ {x:.2f}")

    total_bonification_per_rule['Total'] = total_bonification_per_rule['Total'].apply(lambda x: f"S/ {x:.2f}")

    return total_bonification_per_rule
#     # Append the new data to the existing bonification_rules in session state
#     st.session_state['bonification_rules'] = pd.concat(
#         [st.session_state['bonification_rules'], new_rules_df],
#         ignore_index=True
#     )
    
#     st.success("Reglas de bonificación cargadas correctamente desde el archivo.")

#     # Optionally clear the file uploader after processing to avoid double uploads
#     st.session_state["uploader_key"] += 1
#     st.rerun()
#     st.write


# # Function to add bonification rules
# def add_bonification_rule(base_product_code, base_product_quantity, bonification_product_code, bonification_quantity, cost, start_date, end_date):
#         global bonification_rules
#         new_rule = pd.DataFrame({
#                 'Base_Product_Code': [base_product_code],
#                 'Base_Product_Quantity': [base_product_quantity],
#                 'Bonification_Product_Code': [bonification_product_code],
#                 'Bonification_Quantity': [bonification_quantity],
#                 'Cost': [cost],
#                 'Start_Date': [pd.to_datetime(start_date)],
#                 'End_Date': [pd.to_datetime(end_date)],
#                 'Status': 1
#         })
#         st.session_state['bonification_rules'] = pd.concat([bonification_rules, new_rule], ignore_index=True)

# def add_combination_bonification_rule(base_product_code, base_product_quantity, bonification_product_code, bonification_quantity, cost, start_date, end_date):
#     global combination_bonification_rules
#     # Create a new rule
#     new_combination_rule = pd.DataFrame({
#         'Base_Product_Code': [base_product_code],
#         'Base_Product_Quantity': [base_product_quantity],
#         'Bonification_Product_Code': [bonification_product_code],
#         'Bonification_Quantity': [bonification_quantity],
#         'Cost': [cost],
#         'Start_Date': [pd.to_datetime(start_date)],  # Convert to datetime
#         'End_Date': [pd.to_datetime(end_date)],       # Convert to datetime
#         'Status': 1
#     })
#     # Append the new rule to the existing DataFrame
#     st.session_state['combination_bonification_rules'] = pd.concat([combination_bonification_rules, new_combination_rule], ignore_index=True)

# # Function to delete bonification rules based on indices
# def delete_bonification_rule(indices):
#     global bonification_rules
#     bonification_rules = bonification_rules.drop(indices).reset_index(drop=True)
#     st.session_state['bonification_rules'] = bonification_rules

# # Streamlit form to collect user input
# st.title("Gestión de Reglas")

# registro_regla=st.selectbox('Escoja una Opción',('Regla Simple','Regla Combinada'))
# if registro_regla=='Regla Simple':
#         st.subheader("Regla Simple")
# elif registro_regla=='Regla Combinada':
#         st.subheader("Regla Combinada")

# with st.form("bonification_rule_form"):
#         base_product_code = st.text_input("Código de Producto Base")
#         base_product_quantity = st.number_input("Cantidad de Producto Base", min_value=1)
#         bonification_product_code = st.text_input("Código de Producto de Bonificación")
#         bonification_quantity = st.number_input("Cantidad de Producto de Bonificación", min_value=1)
#         cost = st.number_input("Costo", min_value=0.0, format="%.2f")
#         start_date = st.date_input("Fecha de Inicio", value=datetime.today())
#         end_date = st.date_input("Fecha Final", value=datetime.today())

#         # Submit button
#         submitted = st.form_submit_button("Agregar Regla")

#         if submitted:
#                 if registro_regla=='Regla Simple':
#                         add_bonification_rule(base_product_code, base_product_quantity, bonification_product_code, bonification_quantity, cost, start_date, end_date)
#                 elif registro_regla=='Regla Simple':
#                         add_combination_bonification_rule(base_product_code, base_product_quantity, bonification_product_code, bonification_quantity, cost, start_date, end_date)

#                 st.success("Regla registrada correctamente!")




# # Display the DataFrame with a checkbox to select rows for deletion
# st.subheader("Reglas Registradas")

# if not bonification_rules.empty:
#     delete_indices = st.multiselect("Seleccione las reglas a Eliminar", bonification_rules.index, format_func=lambda x: f"Regla {x+1}", placeholder='Escoja una regla')

#     if st.button("Borrar regla seleccionada"):
#         delete_bonification_rule(delete_indices)
#         st.success(f"Regla(s) Eliminadas(s): {', '.join(map(str, delete_indices))}")

#     st.write(bonification_rules)
# else:
#     st.write("Sin Reglas Registradas.")

# def apply_bonification_rules_per_sale2(sales_df):
#     bonification_summary = []

#     for nro_doc, group in sales_df.groupby('Pedido'):
#         applied_rules = []

#         for index, rule in bonification_rules.sort_values(by='Base_Product_Quantity', ascending=False).iterrows():
#             sale_dates = group['Emision'].dt.date.unique()
#             for sale_date in sale_dates:
#                 if rule['Start_Date'].date() <= sale_date <= rule['End_Date'].date():
#                     base_product_sales = group[group['Cod. Art.'] == rule['Base_Product_Code']]
#                     total_base_quantity = base_product_sales['Cantidad'].sum()
#                     bonification_multiplier = total_base_quantity // rule['Base_Product_Quantity']

#                     if total_base_quantity >= rule['Base_Product_Quantity'] and bonification_multiplier > 0 and rule['Bonification_Product_Code'] not in applied_rules:
#                         bonification_product_sales = group[group['Cod. Art.'] == rule['Bonification_Product_Code']]
#                         total_bonification_quantity = bonification_product_sales['Cantidad'].sum()
#                         bonification_cost = rule['Cost']

#                         bonification_entry = {
#                             'Nro Documento': nro_doc,
#                             'Base_Product_Code': rule['Base_Product_Code'],
#                             'Bonification_Product_Code': rule['Bonification_Product_Code'],
#                             'Quantity': total_bonification_quantity,
#                             'Total': total_bonification_quantity * bonification_cost,
#                             'Cost': bonification_cost,
#                             'Rule_Applied': f"{rule['Bonification_Product_Code']} (Buy {rule['Base_Product_Quantity']} of {rule['Base_Product_Code']}, get {rule['Bonification_Quantity']} of {rule['Bonification_Product_Code']})"
#                         }

#                         bonification_summary.append(bonification_entry)
#                         applied_rules.append(rule['Bonification_Product_Code'])

#     bonification_summary_df = pd.DataFrame(bonification_summary)

#     total_bonification_per_rule = bonification_summary_df.groupby(
#         ['Base_Product_Code', 'Bonification_Product_Code', 'Rule_Applied', 'Cost']
#     ).agg(
#         Total_Quantity=('Quantity', 'sum'),
#         Total_Value=('Total', 'sum'),
#     ).reset_index()

#     return total_bonification_per_rule

# if uploaded_file is None or monthFile is None or supplierFile is None or bonification_rules.empty:

#     submittedTable = st.button("Mostrar Tabla", disabled=True)
# else:
#     submittedTable = st.button("Mostrar Tabla", disabled=False)

# if submittedTable:
#         with st.spinner("Procesando"):
#                 df = pd.read_excel(uploaded_file)
#                 if 'Emision' in df.columns:
#                         df['Emision'] = pd.to_datetime(df['Emision'], errors='coerce')  # Convert to datetime format

#                 # Clean the DataFrame by removing rows where 'Tipo Pedido' is NaN
#                 df_dropNull = df.dropna(subset=['Tipo Pedido'])

#                 # Drop unnecessary columns
#                 df_cutColumns = df_dropNull.drop(['TD', 'Cod. Ruteo', 'RUC/DNI'], axis=1)

#                 # Filter by 'Proveedor' = 'ETE'
#                 dfProvider = df_cutColumns[df_cutColumns['Proveedor'] == 'ETE']

#                 # Filter by the selected month in 'Emision'
#                 month_rows = dfProvider[dfProvider['Emision'].dt.month == 8]

#                 # Display the filtered DataFrame
#                 st.subheader(f"Data del mes {monthFile}")
#                 st.write(month_rows)
#         bonificationTable = apply_bonification_rules_per_sale2(month_rows)
        
#         st.write(bonificationTable)
