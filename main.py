"""
Portfolio Management System - Python Tkinter Application
Created: December 2024 - January 2025
Database Management System Project

Requirements:
- Python 3.x
- mysql-connector-python: pip install mysql-connector-python
- tkinter (usually comes with Python)

Database Configuration:
Update the DB_CONFIG dictionary with your MySQL credentials
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from datetime import datetime
from decimal import Decimal

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Change this
    'database': 'portfolio_management'
}

class DatabaseConnection:
    """Handle database connections and queries"""
    
    @staticmethod
    def get_connection():
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None, fetch=True):
        conn = DatabaseConnection.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.rowcount
            
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as e:
            messagebox.showerror("Query Error", f"Query failed: {e}")
            return None

class PortfolioManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2c3e50')
        
        # Style configuration
        self.setup_styles()
        
        # Current user
        self.current_user = None
        
        # Create main container
        self.main_container = ttk.Frame(root, padding="10")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(1, weight=1)
        
        # Show login screen
        self.show_login()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'), 
                       background='#2c3e50', foreground='#ecf0f1')
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'),
                       background='#34495e', foreground='#ecf0f1')
        style.configure('TButton', font=('Helvetica', 10), padding=5)
        style.configure('Action.TButton', font=('Helvetica', 10, 'bold'))
        
    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def show_login(self):
        self.clear_container()
        
        # Title
        title = ttk.Label(self.main_container, text="Portfolio Management System",
                         style='Title.TLabel')
        title.grid(row=0, column=0, pady=20)
        
        # Login frame
        login_frame = ttk.LabelFrame(self.main_container, text="User Login", padding="20")
        login_frame.grid(row=1, column=0, padx=20, pady=20)
        
        # Email entry
        ttk.Label(login_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(login_frame, width=30)
        self.email_entry.grid(row=0, column=1, pady=5, padx=5)
        self.email_entry.insert(0, "john.doe@email.com")  # Default for testing
        
        # Login button
        login_btn = ttk.Button(login_frame, text="Login", command=self.login,
                              style='Action.TButton')
        login_btn.grid(row=1, column=0, columnspan=2, pady=10)
        
        # New user button
        new_user_btn = ttk.Button(login_frame, text="Register New User",
                                  command=self.show_registration)
        new_user_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Test connection button
        test_btn = ttk.Button(login_frame, text="Test Database Connection",
                             command=self.test_connection)
        test_btn.grid(row=3, column=0, columnspan=2, pady=10)
    
    def test_connection(self):
        conn = DatabaseConnection.get_connection()
        if conn:
            messagebox.showinfo("Success", "Database connection successful!")
            conn.close()
    
    def login(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showerror("Error", "Please enter an email address")
            return
        
        query = "SELECT * FROM Users WHERE email = %s AND status = 'active'"
        result = DatabaseConnection.execute_query(query, (email,))
        
        if result and len(result) > 0:
            self.current_user = result[0]
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "User not found or account inactive")
    
    def show_registration(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Register New User")
        reg_window.geometry("400x500")
        
        frame = ttk.Frame(reg_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input fields
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Date of Birth (YYYY-MM-DD):", "dob"),
            ("Address:", "address")
        ]
        
        entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            entries[field] = entry
        
        def register():
            query = """INSERT INTO Users (first_name, last_name, email, phone, 
                      date_of_birth, address) VALUES (%s, %s, %s, %s, %s, %s)"""
            params = (
                entries['first_name'].get(),
                entries['last_name'].get(),
                entries['email'].get(),
                entries['phone'].get(),
                entries['dob'].get(),
                entries['address'].get()
            )
            
            result = DatabaseConnection.execute_query(query, params, fetch=False)
            if result:
                messagebox.showinfo("Success", "User registered successfully!")
                reg_window.destroy()
        
        ttk.Button(frame, text="Register", command=register,
                  style='Action.TButton').grid(row=len(fields), column=0,
                                              columnspan=2, pady=20)
    
    def show_dashboard(self):
        self.clear_container()
        
        # Header
        header_frame = ttk.Frame(self.main_container)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        welcome_text = f"Welcome, {self.current_user['first_name']} {self.current_user['last_name']}"
        ttk.Label(header_frame, text=welcome_text, style='Header.TLabel').pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="Logout", command=self.show_login).pack(side=tk.RIGHT)
        
        # Notebook for tabs
        notebook = ttk.Notebook(self.main_container)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Create tabs
        self.create_portfolios_tab(notebook)
        self.create_holdings_tab(notebook)
        self.create_transactions_tab(notebook)
        self.create_assets_tab(notebook)
        self.create_watchlist_tab(notebook)
        self.create_reports_tab(notebook)
    
    def create_portfolios_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="My Portfolios")
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(btn_frame, text="Add New Portfolio",
                  command=self.add_portfolio).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh",
                  command=lambda: self.load_portfolios(tree)).pack(side=tk.LEFT)
        
        # Treeview
        columns = ('ID', 'Name', 'Type', 'Total Value', 'Currency', 'Status', 'Holdings')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        
        # Load data
        self.load_portfolios(tree)
    
    def load_portfolios(self, tree):
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        query = "SELECT * FROM v_user_portfolios WHERE user_id = %s"
        portfolios = DatabaseConnection.execute_query(query, (self.current_user['user_id'],))
        
        if portfolios:
            for p in portfolios:
                tree.insert('', tk.END, values=(
                    p['portfolio_id'],
                    p['portfolio_name'],
                    p['portfolio_type'],
                    f"${p['total_value']:,.2f}",
                    'USD',
                    p['status'],
                    p['total_holdings']
                ))
    
    def add_portfolio(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Portfolio")
        dialog.geometry("400x300")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Portfolio Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Portfolio Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(frame, textvariable=type_var, width=28,
                                  values=['aggressive', 'moderate', 'conservative'])
        type_combo.grid(row=1, column=1, pady=5)
        type_combo.set('moderate')
        
        ttk.Label(frame, text="Initial Value:").grid(row=2, column=0, sticky=tk.W, pady=5)
        value_entry = ttk.Entry(frame, width=30)
        value_entry.grid(row=2, column=1, pady=5)
        value_entry.insert(0, "0.00")
        
        def save_portfolio():
            query = """INSERT INTO Portfolios (user_id, portfolio_name, portfolio_type, total_value)
                      VALUES (%s, %s, %s, %s)"""
            params = (
                self.current_user['user_id'],
                name_entry.get(),
                type_var.get(),
                float(value_entry.get())
            )
            
            result = DatabaseConnection.execute_query(query, params, fetch=False)
            if result:
                messagebox.showinfo("Success", "Portfolio created successfully!")
                dialog.destroy()
        
        ttk.Button(frame, text="Save", command=save_portfolio,
                  style='Action.TButton').grid(row=3, column=0, columnspan=2, pady=20)
    
    def create_holdings_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="Portfolio Holdings")
        
        # Portfolio selection
        select_frame = ttk.Frame(frame)
        select_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(select_frame, text="Select Portfolio:").pack(side=tk.LEFT, padx=5)
        self.portfolio_var = tk.StringVar()
        portfolio_combo = ttk.Combobox(select_frame, textvariable=self.portfolio_var, width=30)
        portfolio_combo.pack(side=tk.LEFT, padx=5)
        
        # Load portfolios into combobox
        portfolios = DatabaseConnection.execute_query(
            "SELECT portfolio_id, portfolio_name FROM Portfolios WHERE user_id = %s",
            (self.current_user['user_id'],)
        )
        if portfolios:
            portfolio_combo['values'] = [f"{p['portfolio_id']} - {p['portfolio_name']}"
                                        for p in portfolios]
        
        # Treeview
        columns = ('Asset', 'Symbol', 'Type', 'Quantity', 'Purchase Price',
                  'Current Value', 'Purchase Date')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        def load_holdings():
            for item in tree.get_children():
                tree.delete(item)
            
            selected = self.portfolio_var.get()
            if not selected:
                return
            
            portfolio_id = int(selected.split(' - ')[0])
            
            query = """
                SELECT a.asset_name, a.asset_symbol, a.asset_type, ph.quantity,
                       ph.purchase_price, ph.current_value, ph.purchase_date
                FROM Portfolio_Holdings ph
                JOIN Assets a ON ph.asset_id = a.asset_id
                WHERE ph.portfolio_id = %s
            """
            holdings = DatabaseConnection.execute_query(query, (portfolio_id,))
            
            if holdings:
                for h in holdings:
                    tree.insert('', tk.END, values=(
                        h['asset_name'],
                        h['asset_symbol'],
                        h['asset_type'],
                        f"{h['quantity']:.2f}",
                        f"${h['purchase_price']:.2f}",
                        f"${h['current_value']:.2f}",
                        h['purchase_date']
                    ))
        
        ttk.Button(select_frame, text="Load Holdings",
                  command=load_holdings).pack(side=tk.LEFT, padx=5)
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
    
    def create_transactions_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="Transactions")
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(btn_frame, text="Add Transaction",
                  command=self.add_transaction).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        columns = ('ID', 'Portfolio', 'Asset', 'Type', 'Quantity',
                  'Price', 'Total', 'Date', 'Fees')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=90)
        
        tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Load transactions
        query = """
            SELECT t.transaction_id, p.portfolio_name, a.asset_symbol,
                   t.transaction_type, t.quantity, t.price_per_unit,
                   t.total_amount, t.transaction_date, t.fees
            FROM Transactions t
            JOIN Portfolios p ON t.portfolio_id = p.portfolio_id
            JOIN Assets a ON t.asset_id = a.asset_id
            WHERE p.user_id = %s
            ORDER BY t.transaction_date DESC
            LIMIT 100
        """
        transactions = DatabaseConnection.execute_query(query, (self.current_user['user_id'],))
        
        if transactions:
            for t in transactions:
                tree.insert('', tk.END, values=(
                    t['transaction_id'],
                    t['portfolio_name'],
                    t['asset_symbol'],
                    t['transaction_type'],
                    f"{t['quantity']:.2f}",
                    f"${t['price_per_unit']:.2f}",
                    f"${t['total_amount']:.2f}",
                    t['transaction_date'],
                    f"${t['fees']:.2f}"
                ))
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
    
    def add_transaction(self):
        messagebox.showinfo("Feature", "Transaction form would open here.\n"
                           "This would allow buying/selling assets.")
    
    def create_assets_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="Available Assets")
        
        # Search frame
        search_frame = ttk.Frame(frame)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Treeview
        columns = ('Symbol', 'Name', 'Type', 'Category', 'Price', 'Exchange', 'Last Updated')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        def load_assets():
            for item in tree.get_children():
                tree.delete(item)
            
            search_term = search_entry.get()
            if search_term:
                query = """
                    SELECT a.*, ac.category_name
                    FROM Assets a
                    JOIN Asset_Categories ac ON a.category_id = ac.category_id
                    WHERE a.asset_name LIKE %s OR a.asset_symbol LIKE %s
                """
                assets = DatabaseConnection.execute_query(query,
                    (f"%{search_term}%", f"%{search_term}%"))
            else:
                query = """
                    SELECT a.*, ac.category_name
                    FROM Assets a
                    JOIN Asset_Categories ac ON a.category_id = ac.category_id
                    LIMIT 100
                """
                assets = DatabaseConnection.execute_query(query)
            
            if assets:
                for a in assets:
                    tree.insert('', tk.END, values=(
                        a['asset_symbol'],
                        a['asset_name'],
                        a['asset_type'],
                        a['category_name'],
                        f"${a['current_price']:.2f}",
                        a['exchange'],
                        a['last_updated']
                    ))
        
        ttk.Button(search_frame, text="Search",
                  command=load_assets).pack(side=tk.LEFT, padx=5)
        
        load_assets()  # Initial load
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
    
    def create_watchlist_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="Watchlist")
        
        ttk.Label(frame, text="Track assets you're interested in",
                 font=('Helvetica', 12)).grid(row=0, column=0, pady=10)
        
        # Treeview
        columns = ('Asset', 'Symbol', 'Current Price', 'Target Price',
                  'Date Added', 'Notes')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Load watchlist
        query = """
            SELECT a.asset_name, a.asset_symbol, a.current_price,
                   w.target_price, w.added_date, w.notes
            FROM Watchlist w
            JOIN Assets a ON w.asset_id = a.asset_id
            WHERE w.user_id = %s
        """
        watchlist = DatabaseConnection.execute_query(query, (self.current_user['user_id'],))
        
        if watchlist:
            for w in watchlist:
                tree.insert('', tk.END, values=(
                    w['asset_name'],
                    w['asset_symbol'],
                    f"${w['current_price']:.2f}",
                    f"${w['target_price']:.2f}" if w['target_price'] else "N/A",
                    w['added_date'],
                    w['notes'] or ""
                ))
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
    
    def create_reports_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="Reports & Analytics")
        
        # Performance summary
        perf_frame = ttk.LabelFrame(frame, text="Portfolio Performance", padding="10")
        perf_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        query = """
            SELECT p.portfolio_name, 
                   SUM(ph.quantity * a.current_price) AS current_value,
                   SUM(ph.current_value) AS cost_basis,
                   SUM(ph.quantity * a.current_price) - SUM(ph.current_value) AS gain_loss
            FROM Portfolios p
            JOIN Portfolio_Holdings ph ON p.portfolio_id = ph.portfolio_id
            JOIN Assets a ON ph.asset_id = a.asset_id
            WHERE p.user_id = %s AND p.status = 'active'
            GROUP BY p.portfolio_id
        """
        performance = DatabaseConnection.execute_query(query, (self.current_user['user_id'],))
        
        if performance:
            row = 0
            for p in performance:
                ttk.Label(perf_frame, text=p['portfolio_name'],
                         font=('Helvetica', 11, 'bold')).grid(row=row, column=0,
                                                              sticky=tk.W, padx=5)
                
                current = float(p['current_value']) if p['current_value'] else 0
                cost = float(p['cost_basis']) if p['cost_basis'] else 0
                gain = float(p['gain_loss']) if p['gain_loss'] else 0
                
                info = f"Value: ${current:,.2f} | Cost: ${cost:,.2f} | "
                info += f"Gain/Loss: ${gain:,.2f}"
                
                if cost > 0:
                    pct = (gain / cost) * 100
                    info += f" ({pct:+.2f}%)"
                
                ttk.Label(perf_frame, text=info).grid(row=row, column=1,
                                                      sticky=tk.W, padx=20)
                row += 1
        else:
            ttk.Label(perf_frame, text="No portfolio data available").grid(row=0, column=0)
        
        # Summary statistics
        stats_frame = ttk.LabelFrame(frame, text="Account Summary", padding="10")
        stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Total portfolios
        portfolio_count = DatabaseConnection.execute_query(
            "SELECT COUNT(*) as count FROM Portfolios WHERE user_id = %s",
            (self.current_user['user_id'],)
        )
        
        # Total assets
        asset_count = DatabaseConnection.execute_query(
            """SELECT COUNT(DISTINCT ph.asset_id) as count
               FROM Portfolio_Holdings ph
               JOIN Portfolios p ON ph.portfolio_id = p.portfolio_id
               WHERE p.user_id = %s""",
            (self.current_user['user_id'],)
        )
        
        stats = [
            f"Total Portfolios: {portfolio_count[0]['count'] if portfolio_count else 0}",
            f"Total Assets Held: {asset_count[0]['count'] if asset_count else 0}",
            f"Member Since: {self.current_user['registration_date'].strftime('%Y-%m-%d')}"
        ]
        
        for i, stat in enumerate(stats):
            ttk.Label(stats_frame, text=stat, font=('Helvetica', 10)).grid(
                row=i, column=0, sticky=tk.W, pady=2)
        
        frame.columnconfigure(0, weight=1)

def main():
    root = tk.Tk()
    app = PortfolioManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
