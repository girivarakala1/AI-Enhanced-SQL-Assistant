import streamlit as st
from lonchain_connection import get_few_shot_db_chain

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",

    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

def main():
    tab1, tab2= st.tabs(["Home","Database Q&A "])

    with tab1:
        st.title("Bike Store Relational Database | SQL")
        st.image("C:\\Users\\giriv\\OneDrive\\Desktop\\bikes.jpg")
        st.write("The brands table stores the brand’s information of bikes, for example, Electra, Haro, and Heller.")
        st.write("The categories table stores the bike’s categories such as children bicycles, comfort bicycles, and electric bikes.")
        st.write("The customers table stores customer’s information including first name, last name, phone, email, street, city, state and zip code.")
        st.write("The order_items table stores the line items of a sales order. Each line item belongs to a sales order specified by the order_id column. A sales order line item includes product, order quantity, list price, and discount.")
        st.write("The orders table stores the sales order’s header information including customer, order status, order date, required date, shipped date. It also stores the information on where the sales transaction was created (store) and who created it (staff). Each sales order has a row in the sales_orders table. A sales order has one or many line items stored in the order_items table.")
        st.write("The products table stores the product’s information such as name, brand, category, model year, and list price. Each product belongs to a brand specified by the brand_id column. Hence, a brand may have zero or many products.Each product also belongs a category specified by the category_id column. Also, each category may have zero or many products.")
        st.write("The staffs table stores the essential information of staffs including first name, last name. It also contains the communication information such as email and phone.")
        st.write("The stocks table stores the inventory information i.e. the quantity of a particular product in a specific store.")
        st.write("The stores table includes the store’s information. Each store has a store name, contact information such as phone and email, and an address including street, city, state, and zip code.")
        st.write("ok")

    with tab2:
        st.write("Examples:")
        st.write("Write a query to find the total quantity of each product available in all stores?")
        question = st.text_input("Question: ")

        if question:
            chain = get_few_shot_db_chain()
            response = chain.run(question)

            st.header("Answer")
            results = response.split(",")
            for result in results:
                st.write(result)




if __name__ == "__main__":
     main()




