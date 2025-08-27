# SQLite + Pandas CSV Import

This project demonstrates how to import data from a CSV file into a SQLite database using **Python**, **Pandas**, and the built-in `sqlite3` library.  

## 🚀 How It Works
1. Reads a CSV file (`import_test.csv`) stored in the `data/` folder using Pandas.  
2. Creates a SQLite table (`datos`) if it doesn’t exist.  
3. Iterates through the rows of the DataFrame and inserts them into the database.  
4. Commits the changes and allows you to query sample data.

## 🛠 Requirements
- Python 3.8+
- Pandas 2.0.3

## 🛠 How to run

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment (macOs / Linux):
```bash
source venv/bin/activate
```

Activate the virtual environment (Windows):
```bash
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the project:
```bash
python main.py
```

## Design Decisions and Assumptions

The following suggestions were applied during the creation of the database table:

1. **CSV Input Handling**  
   - The dataset is read from the `data/import_test.csv` file using `;` as the delimiter:
     ```python
     df = pd.read_csv("data/import_test.csv", sep=";")
     ```

2. **Column Transformation**  
   - The column **`coeficiente`** is extracted from the last element of the `name` field.  
   - The `name` field is updated to remove the extracted `coeficiente`.  
     ```python
     df["coeficiente"] = df["name"].apply(lambda x: x.split(" ")[-1])
     df["name"] = df["name"].apply(lambda x: " ".join(x.split(" ")[:-1]))
     ```

3. **Data Cleaning and Type Conversion**  
   - The decimal separator in `coeficiente` is converted from `,` to `.`.  
   - `coeficiente` is cast to `float`, and `score` is cast to `int`.  
     ```python
     df["coeficiente"] = df["coeficiente"].apply(lambda x: x.replace(",", "."))
     df["coeficiente"] = df["coeficiente"].astype(float)
     df["score"] = df["score"].astype(int)
     ```

4. **Database Creation**  
   - An SQLite database `datos_interview.db` is created.  
   - A table `datos` is defined with columns: `id`, `name`, `brand`, `score`, and `probability`.  
     ```sql
     CREATE TABLE IF NOT EXISTS 
         datos(id INT,
               name VARCHAR(50),
               brand VARCHAR(50),
               score INT,
               probability REAL)
     ```
5. **Validation**  
   - A sample query retrieves the first 5 rows to verify the inserted data:  
     ```python
     cur.execute("SELECT * FROM datos LIMIT 5")
     rows = cur.fetchall()
     ```

---

### Assumptions Made
- The input CSV file always contains the columns `id`, `name`, `brand`, and `score`.  
- The `name` field always ends with a numerical value (`coeficiente`).  
- `score` values are numeric and can be safely converted to integers.  
- The database is local (`sqlite3`) and does not require advanced configurations.  
