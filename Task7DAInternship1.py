import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

try:
    # Step 1: Connect to the SQLite database
    conn = sqlite3.connect("sales_database.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        category TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        total_sales REAL GENERATED ALWAYS AS (quantity * price) STORED,
        sale_date DATE NOT NULL
    )
''')

# Insert expanded sample sales data
    cursor.executemany('''
    INSERT INTO sales (product, category, quantity, price, sale_date) VALUES (?, ?, ?, ?, ?)
''', [
    ("Laptop", "Electronics", 3, 65000, "2025-04-01"),
    ("Smartphone", "Electronics", 5, 30000, "2025-04-02"),
    ("Tablet", "Electronics", 2, 25000, "2025-04-03"),
    ("Desk Chair", "Furniture", 4, 5500, "2025-04-05"),
    ("Office Table", "Furniture", 2, 12000, "2025-04-06"),
    ("Coffee Maker", "Appliances", 1, 4500, "2025-04-07"),
    ("Headphones", "Electronics", 6, 2500, "2025-04-08"),
    ("Fitness Band", "Wearables", 3, 8000, "2025-04-09"),
    ("Projector", "Electronics", 1, 45000, "2025-04-10"),
    ("Bookshelf", "Furniture", 2, 7500, "2025-04-11"),
    ("Gaming Console", "Electronics", 2, 40000, "2025-04-12"),
    ("Refrigerator", "Appliances", 1, 52000, "2025-04-13"),
    ("Microwave", "Appliances", 2, 15000, "2025-04-14"),
    ("Air Conditioner", "Appliances", 1, 35000, "2025-04-15"),
    ("Smartwatch", "Wearables", 4, 12000, "2025-04-16"),
    ("Electric Kettle", "Appliances", 3, 3000, "2025-04-17"),
    ("Bluetooth Speaker", "Electronics", 5, 4500, "2025-04-18"),
    ("Dining Table", "Furniture", 1, 27000, "2025-04-19"),
    ("Television", "Electronics", 2, 58000, "2025-04-20"),
    ("Gaming Laptop", "Electronics", 1, 95000, "2025-04-21")
])
    
    print("✅ Sales database and table created, and sample data inserted successfully!")
    
    # Step 2: OPTIONAL - Show table columns (debugging help)
    print("\n📋 Table Structure:")
    cursor.execute("PRAGMA table_info(sales)")
    for col in cursor.fetchall():
        print(col)

    # Step 3: SQL query to summarize sales
    query = """
    SELECT 
        product, 
        SUM(quantity) AS total_qty, 
        SUM(quantity * price) AS revenue 
    FROM sales 
    GROUP BY product
    """

    # Step 4: Load result into a pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Step 5: Print the result
    print("\n📊 Sales Summary:")
    print(df)

    # Step 6: Plot bar chart (product vs revenue)
    plt.figure(figsize=(12, 7))
    bars = plt.bar(df['product'], df['revenue'], color='blue')

    # Add labels on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, round(yval, 2),
                 ha='center', va='bottom', fontsize=9)

    # Chart formatting
    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    

    # Save and show the chart
    plt.savefig("sales_chart.png")
    print("\n✅ Chart saved as 'sales_chart.png'")
    plt.show()

except Exception as e:
    print("❌ Error occurred:", e)

finally:
    # Step 7: Always close the connection
    if 'conn' in locals():
        conn.close()
        print("\n🔒 Database connection closed.")
